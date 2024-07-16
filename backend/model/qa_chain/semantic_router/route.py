from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer
from semantic_router import Route

# this could be used as an indicator to our chatbot to switch to a more
# conversational prompt
chitchat = Route(
    name="Exemptions And Introduction",
    utterances=[
        "Am I exempt from the RTA?",
    ],
)
chitchat = Route(
    name="Tenancy Agreement",
    utterances=[
        "What information must a landlord provide?",
        "What are the contents of a tenancy agreement?"
    ],
)

chitchat = Route(
    name="Responsibilities Of A Landlord",
    utterances=[
        "",
    ],
)

chitchat = Route(
    name="Responsibilities Of A Tenant",
    utterances=[
        "",
    ],
)

chitchat = Route(
    name="Security Of Tenure And Termination Of Tenancy",
    utterances=[
        "",
    ],
)

chitchat = Route(
    name="Non Profit Housing CO-OP - Termination Of Occupancy",
    utterances=[
        "",
    ],
)

chitchat = Route(
    name="Assignment, Subletting And Unauthorized Occupancy",
    utterances=[
        "",
    ],
)

chitchat = Route(
    name="Rent Rules",
    utterances=[
        "",
    ],
)

routes = [politics, chitchat]

path = "../../citation_embed/saved_models/"
encoder = HuggingFaceEncoder(model_name=path+"jinaai/jina-embeddings-v2-base-en")

rl = RouteLayer(encoder=encoder, routes=routes)

print(rl("don't you love politics? Hows the weather today?").name)