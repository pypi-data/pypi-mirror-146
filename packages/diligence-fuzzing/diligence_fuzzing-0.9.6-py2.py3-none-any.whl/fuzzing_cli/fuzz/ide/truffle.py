import json
import os
from functools import lru_cache
from json import JSONDecodeError
from os.path import abspath
from pathlib import Path
from subprocess import Popen, TimeoutExpired
from tempfile import TemporaryFile
from typing import Any, Dict, List, Tuple

from fuzzing_cli.fuzz.exceptions import BuildArtifactsError
from fuzzing_cli.fuzz.ide.generic import Contract, IDEArtifacts, Source
from fuzzing_cli.fuzz.options import FuzzingOptions
from fuzzing_cli.util import LOGGER


class TruffleArtifacts(IDEArtifacts):
    def __init__(
        self,
        options: FuzzingOptions,
        targets: List[str],
        build_dir: Path,
        map_to_original_source: bool = False,
    ):
        super(TruffleArtifacts, self).__init__(
            options,
            targets,
            build_dir or Path("./build/contracts"),
            map_to_original_source,
        )
        project_dir = str(Path.cwd().absolute())
        self.build_files_by_source_file = self._get_build_artifacts(self.build_dir)
        self.project_sources = self._get_project_sources(project_dir)
        # targets could be specified using relative path. But sourcePath in truffle artifacts
        # will use absolute paths, so we need to use absolute paths in targets as well
        self._include = [abspath(fp) for fp in self._include]

    @classmethod
    def get_name(cls) -> str:
        return "truffle"

    @classmethod
    def validate_project(cls) -> bool:
        root_dir = Path.cwd().absolute()
        files = list(os.walk(root_dir))[0][2]
        return "truffle-config.js" in files

    @property
    def contracts(self) -> List[Contract]:
        return self.fetch_data()[0]

    @property
    def sources(self) -> Dict[str, Source]:
        return self.fetch_data()[1]

    @lru_cache(maxsize=1)
    def fetch_data(self) -> Tuple[List[Contract], Dict[str, Source]]:
        result_contracts = {}
        result_sources = {}
        for source_file, contracts in self.build_files_by_source_file.items():
            if source_file not in self._include:
                continue
            result_contracts[source_file] = []
            for contract in contracts:
                ignored_sources = set()
                for generatedSource in contract.get("deployedGeneratedSources", []):
                    if generatedSource["language"].lower() == "yul" and type(
                        generatedSource["id"] is int
                    ):
                        ignored_sources.add(generatedSource["id"])
                # We get the build items from truffle and rename them into the properties used by the FaaS
                try:
                    result_contracts[source_file] += [
                        {
                            "sourcePaths": {
                                i: k
                                for i, k in enumerate(
                                    self.project_sources[contract["contractName"]]
                                )
                            },
                            "deployedSourceMap": contract["deployedSourceMap"],
                            "deployedBytecode": contract["deployedBytecode"],
                            "sourceMap": contract["sourceMap"],
                            "bytecode": contract["bytecode"],
                            "contractName": contract["contractName"],
                            "mainSourceFile": contract["sourcePath"],
                            "ignoredSources": list(ignored_sources),
                        }
                    ]
                except KeyError as e:
                    raise BuildArtifactsError(
                        f"Build artifact did not contain expected key. Contract: {contract}: \n{e}"
                    )

                for file_index, source_file_dep in enumerate(
                    self.project_sources[contract["contractName"]]
                ):
                    if source_file_dep in result_sources.keys():
                        continue

                    if source_file_dep not in self.build_files_by_source_file:
                        LOGGER.debug(f"{source_file} not found.")
                        continue

                    # We can select any dict on the build_files_by_source_file[source_file] array
                    # because the .source and .ast values will be the same in all.
                    target_file = self.build_files_by_source_file[source_file_dep][0]
                    result_sources[source_file_dep] = {
                        "fileIndex": file_index,
                        "source": target_file["source"],
                        "ast": target_file["ast"],
                    }
        return self.flatten_contracts(result_contracts), result_sources

    def query_truffle_db(self, query: str, project_dir: str) -> Dict[str, Any]:
        executables = ["truffle", "node_modules/.bin/truffle"]
        if self._options.truffle_executable_path:
            LOGGER.debug(
                f'Got user-provided Truffle executable path "{self._options.truffle_executable_path}"'
            )
            executables.insert(0, self._options.truffle_executable_path)
        _executables = executables[::-1]
        with TemporaryFile() as stdout_file, TemporaryFile() as stderr_file:
            while _executables:
                try:
                    executable = _executables.pop()
                    LOGGER.debug(f'Invoking truffle executable at path "{executable}"')
                    # here we're using the tempfile to overcome the subprocess.PIPE's buffer size limit (65536 bytes).
                    # This limit becomes a problem on a large sized output which will be truncated, resulting to an invalid json
                    with Popen(
                        [executable, "db", "query", f"{query}"],
                        stdout=stdout_file,
                        stderr=stderr_file,
                        cwd=project_dir,
                    ) as p:
                        p.communicate(timeout=3 * 60)
                    if stdout_file.tell() == 0:
                        error = ""
                        if stderr_file.tell() > 0:
                            stderr_file.seek(0)
                            error = str(stderr_file.read())
                        LOGGER.debug(
                            f'Empty response from the Truffle DB.\nQuery: "{query}" \nError: {error}'
                        )
                        return {}

                    stdout_file.seek(0)
                    result = json.load(stdout_file)
                    if not result.get("data"):
                        LOGGER.debug(
                            f'Empty response from the Truffle DB.\nQuery: "{query}" \nRaw response: {stdout_file.read()}'
                        )
                        return {}
                    return result.get("data")
                except FileNotFoundError:
                    # try next executable path
                    continue
                except JSONDecodeError:
                    stdout_file.seek(0)
                    LOGGER.debug(
                        f'JSONDecodeError. \nQuery: "{query}" \nRaw response: {stdout_file.read()}'
                    )
                except TimeoutExpired:
                    LOGGER.debug(f'Truffle DB query timeout.\nQuery: "{query}"')
                except Exception as e:
                    stdout_file.seek(0)
                    LOGGER.debug(
                        f'Truffle DB query error.\nQuery: "{query}". \nRaw result: {stdout_file.read()}\nError: {e}'
                    )
                return {}

            raise BuildArtifactsError(
                f"Truffle DB connection error. Tried executable at paths: {executables}. "
                f"Please make sure truffle is installed properly or provide path "
                f"to a truffle executable using `--truffle-path` option to `fuzz run`"
            )

    def _get_project_sources(self, project_dir: str) -> Dict[str, List[str]]:
        result = self.query_truffle_db(
            f'query {{ projectId(input: {{ directory: "{project_dir}" }}) }}',
            project_dir,
        )
        project_id = result.get("projectId")

        if not project_id:
            LOGGER.debug(f'No project artifacts found. Path: "{project_dir}"')
            raise BuildArtifactsError(
                "No project artifacts found. "
                "Please make sure that your local truffle configuration has Truffle DB enabled"
            )

        result = self.query_truffle_db(
            f"""
            {{
              project(id:"{project_id}") {{
                contracts {{
                  name
                  compilation {{
                    processedSources {{
                      source {{
                        sourcePath
                      }}
                    }}
                  }}
                }}
              }}
            }}
            """,
            project_dir,
        )

        contracts = {}

        if (
            not result.get("project")
            or not result["project"]["contracts"]
            or len(result["project"]["contracts"]) == 0
        ):
            LOGGER.debug(
                f'No project artifacts found. Path: "{project_dir}". Project ID "{project_id}"'
            )
            raise BuildArtifactsError(
                "No project artifacts found. "
                "Please make sure that your local truffle configuration has Truffle DB enabled"
            )

        for contract in result["project"]["contracts"]:
            contracts[contract["name"]] = list(
                map(
                    lambda x: x["source"]["sourcePath"],
                    contract["compilation"]["processedSources"],
                )
            )
        return contracts

    @staticmethod
    def get_default_build_dir() -> str:
        return "build/contracts"

    @staticmethod
    def get_default_sources_dir() -> str:
        return "contracts"
