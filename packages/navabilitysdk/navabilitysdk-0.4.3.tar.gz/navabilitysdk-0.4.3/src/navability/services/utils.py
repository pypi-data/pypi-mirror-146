import time
from typing import List

from navability.entities import NavAbilityClient
from navability.services import getStatusesLatest


async def waitForCompletion(
    navAbilityClient: NavAbilityClient,
    requestIds: List[str],
    maxSeconds: int = 60,
    expectedStatuses: List[str] = None,
    exceptionMessage: str = "Requests did not complete in time",
):
    """Wait for the requests to complete, poll until done.

    Args:
        requestIds (List[str]): The request IDs that should be polled.
        maxSeconds (int, optional): Maximum wait time. Defaults to 60.
        expectedStatus (str, optional): Expected status message per request.
            Defaults to "Complete".
    """
    if expectedStatuses is None:
        expectedStatuses = ["Complete", "Failed"]
    wait_time = maxSeconds
    tasksComplete = False
    while not tasksComplete:
        statuses = (await getStatusesLatest(navAbilityClient, requestIds)).values()
        tasksComplete = all(s.state in expectedStatuses for s in statuses)
        if tasksComplete:
            break
        else:
            time.sleep(2)
            wait_time -= 2
            if wait_time <= 0:
                raise Exception(exceptionMessage)
