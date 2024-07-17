from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer
from semantic_router import Route

# this could be used as an indicator to our chatbot to switch to a more
# conversational prompt
exemp_and_intro_route = Route(
    name="Exemptions_And_Introduction",
    utterances=[
        "Am I exempt from the RTA?",
        "What includes services and facilities?",
        "What is vital service?",
        "Are students exempt from the RTA?",
        "What are the requirements of a landlord tenant lease agreement",
        "land lease home or social housing exemption",
        "what is a utility?"
    ],
)
tenancy_agreement_route = Route(
    name="Tenancy_Agreement",
    utterances=[
        "What information must a landlord provide?",
        "What are the contents of a tenancy agreement?",
        "Can I withhold the rent?",
        "Can I get my lease agreement in writing?",
        "Can lanlord force me to pay rent?",
        "When does lease agreement come in force?",
        "no pet provision?"
    ],
)

landlord_resp_route = Route(
    name="Responsibilities_Of_A_Landlord",
    utterances=[
        "What is a landlord responsible for?",
        "Is a tenant required to repair?",
        "Can a landlord shut off utilities?",
        "Can a landlord change locks?",
        "Can a landlord enter without a notice?",
        "How late can a landlord give a notice?",
        "Can I complain to the board after moving out?",
        "When can the board force landlord to order, repair, comply with standards?"
    ],
)

tenant_responsibilities = Route(
    name="Responsibilities Of A Tenant",
    utterances=[
        "Is a tenant responsible for cleaning?",
        "What repairs does a tenant need to do?",
        "Can I change the room locks as a tenant?",
        "Can a landlord not allow an AC unit?",
        "Can I have an AC?",
        "Does AC installation affect my rent?",
        "Does a tenant need to tell a landlord about AC installation?"
    ],
)

tenure_security = Route(
    name="Security Of Tenure And Termination Of Tenancy",
    utterances=[
        "",
    ],
)

# part V.1
coop_housing = Route(
    name="Eviction - Coop Housing",
    utterances=[
        "",
    ],
)

assignment_and_subletting = Route(
    name="Assignment, Subletting And Unauthorized Occupancy",
    utterances=[
        "Can another person live in my unit?",
        "Can my landlord deny my sublet?",
        "Am I responsible for my sublet?",
        "Can I assign my unit to someone else?",
        "Landlord denied sublet what can I do",
        "Eviction with termination order",
        "Unauthorized occupancy"
    ],
)

rent_rules = Route(
    name="Rent Rules",
    utterances=[
        "",
    ],
)

# part 8
rent_rules = Route(
    name="Utility Cost",
    utterances=[
        "In what cases can a landlord shut off electicity, water, or heat?",
        "Can I get a rent decrease if I have no electricity, water, or heat utilites?",
        "Is there a deposit for utilities?",
        "Can a landlord charge for part of the utilities?",        
    ],
)

# part 9
care_homes = Route(
    name="Care Homes",
    utterances=[
        "",
    ],
)
routes = [exemp_and_intro_route, tenancy_agreement_route, landlord_resp_route]

path = "../../citation_embed/saved_models/"
encoder = HuggingFaceEncoder(model_name=path+"jinaai/jina-embeddings-v2-base-en")
rl = RouteLayer(encoder=encoder, routes=routes)


def identify_collections(query):
    results = rl.retrieve_multiple_routes(query)
    names = []
    scores = []
    
    for result in results:
        names.append(result.name)
        scores.append(result.similarity_score)
    return names, scores
    