# Copyright (c) 2016-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import List

from .. import log
from .check import Check


class Analyze(Check):
    NAME = "analyze"

    def __init__(self, arguments, configuration, analysis_directory) -> None:
        super(Analyze, self).__init__(arguments, configuration, analysis_directory)
        self._taint_models_path = (
            arguments.taint_models_path or configuration.taint_models_path
        )
        self._save_results_to = arguments.save_results_to
        self._dump_call_graph = arguments.dump_call_graph

    def _flags(self) -> List[str]:
        flags = super()._flags()
        if self._taint_models_path:
            flags.extend(["-taint-models", self._taint_models_path])
        if self._save_results_to:
            flags.extend(["-save-results-to", self._save_results_to])
        if self._dump_call_graph:
            flags.extend(["-dump-call-graph"])
        return flags

    def _run(self, retries: int = 1) -> None:
        result = self._call_client(command=self.NAME)
        result.check()
        log.stdout.write(result.output)
