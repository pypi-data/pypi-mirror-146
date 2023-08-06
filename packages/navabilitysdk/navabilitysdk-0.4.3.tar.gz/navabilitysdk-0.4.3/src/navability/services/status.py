from typing import List

from gql import gql

from navability.common.queries import GQL_GETSTATUSLATEST, GQL_GETSTATUSMESSAGES
from navability.entities.navabilityclient import NavAbilityClient, QueryOptions
from navability.entities.statusmessage import StatusMessageSchema


async def getStatusMessages(navAbilityClient: NavAbilityClient, id: str):
    """Get all the statuses for a request.

    Args:
        navAbilityClient (NavAbilityClient): The NavAbility client.
        id (str): The ID of the request that you want the statuses on.
    """
    statusMessages = await navAbilityClient.query(
        QueryOptions(gql(GQL_GETSTATUSMESSAGES), {"id": id})
    )
    schema = StatusMessageSchema(many=True)
    return schema.load(statusMessages["statusMessages"])


async def getStatusLatest(navAbilityClient: NavAbilityClient, id: str):
    """Get the latest status message for a request.

    Args:
        navAbilityClient (NavAbilityClient): The NavAbility client.
        id (str): The ID of the request that you want the latest status on.
    """
    statusMessages = await navAbilityClient.query(
        QueryOptions(gql(GQL_GETSTATUSLATEST), {"id": id})
    )
    schema = StatusMessageSchema()
    return schema.load(statusMessages["statusLatest"])


async def getStatusesLatest(navAbilityClient: NavAbilityClient, ids: List[str]):
    """Helper function to get a dictionary of all latest statues for a list of results.

    Args:
        navAbilityClient (NavAbilityClient): The NavAbility client.
        ids (List[str]): A list of the IDS that you want statuses on.
    """
    return {r: await getStatusLatest(navAbilityClient, r) for r in ids}
