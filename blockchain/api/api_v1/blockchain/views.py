from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/", name="View blockchain")
async def blockchain(request: Request):
    node = request.app.state.node
    return node.blockchain.to_dict()
