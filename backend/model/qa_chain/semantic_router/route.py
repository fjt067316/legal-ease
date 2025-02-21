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
    name="Responsibilities_Of_A_Tenant",
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
    name="Security_Of_Tenure_And_Termination_Of_Tenancy",
    utterances=[
        "How can I end my lease?",
        "can my landlord terminate my tenancy?",
        "what are the contents of an eviction notice?",
        "landlord eviction notice or notice of termination",
        "post secondary or university student termination",
        "fixed term or periodic tenancy lease ending what happens?",
        "landlord recovering possesions or taking things from unit",
        "landlord take my stuff because Im not paying rent", # No landlord shall, without legal process, seize a tenant’s property for default in the payment of rent or for the breach of any other obligation of the tenant.
        "can a landlord move me out immediately after an eviction order?",
        "got evicted can I pick up my stuff?",
        "What can the board do if my landlord tries illegal eviction?",
        "definition of violence and abuse of a tenant",
        "what happens if my roomate is violent?",
        "who can my landlord tell about my notice of termination?",
        "While I'm being evicted can my landlord advertise the unit for rent?",
        "Can my landlord evict me for renovations or maintenance?",
        "Conversion to condo right of first refusal",
        "landlord sold condo what rent will I pay?",
        "do I get compensation for eviction from renovation?",
        "bad faith eviction",
        "can I be evicted for drugs or damages?",
        "roomate ruining my reasonable enjoyment can landlord evict him?", #A landlord may give a tenant notice of termination of the tenancy if the conduct of the tenant, another occupant of the rental unit or a person permitted
    ],
)

landlord_evict_app = Route(
    name="Application_by_Landlord_Notice_of_Termination",
    utterances=[
        "When can the landlord apply to the ltb for eviction?",
        "Can I be evicted if the landlord or his friend want to move in?",
        "How does the board determine good faith?",
        "Can the landlord evice me for demolition, conversion, or repairs?",
        "Can I be evicted for not paying rent?",
        "Can the landlord tenant board order me to pay rent?",
        "Can I be evicted for doing something illegal in my unit?",
        "Can I be evicted for having an animal?",
        "Can the landlord apply for eviction without me knowing?",
        "Do I get credit for rent deposit if Im ordered to pay the landlord money?",
        "eviction for abandoment",
        "do eviction notices expire?",
        "what happens if I ignore an eviction notice?",
        "do I have to compensate the landlord for ignoring eviction?",
        "can a landlord apply to the ltb for failure to pay utility costs or ignoring reasonable enjoyment of the unit",
        "can a landlord apply the the board for damage compensation?",
        "death of a tenant or roomate",
        "superintendent premise employment of the tenant"
    ],
)

# part V.1
coop_housing = Route(
    name="Eviction_Non_Profit_Coop_Housing",
    utterances=[
        "Non profit housing co-op",
        "rent geared to income assistane",
        "what happens if I lie about my income while living in a non profit housing coop?"
        
    ],
)

# part 6
assignment_and_subletting = Route(
    name="Assignment_Subletting_Unauthorized_Occupancy",
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

# part 10
care_homes = Route(
    name="Mobile Home Parks",
    utterances=[
        "",
    ],
)

# part 11
care_homes = Route(
    name="The Landlord Tenant Board",
    utterances=[
        "",
    ],
)

# part 12
care_homes = Route(
    name="Board Proceedings",
    utterances=[
        "",
    ],
)

# part 13
care_homes = Route(
    name="municipal vital services",
    utterances=[
        "",
    ],
)

# part 14
care_homes = Route(
    name="maintenance standards",
    utterances=[
        "",
    ],
)

# part 15
care_homes = Route(
    name="administration and enforcement",
    utterances=[
        "",
    ],
)

# part 16
care_homes = Route(
    name="offences",
    utterances=[
        "",
    ],
)

# part 17
care_homes = Route(
    name="regulations",
    utterances=[
        "",
    ],
)

# part 18
care_homes = Route(
    name="transition",
    utterances=[
        "",
    ],
)

routes = [exemp_and_intro_route, tenancy_agreement_route, landlord_resp_route, tenant_responsibilities, tenure_security, landlord_evict_app, coop_housing, assignment_and_subletting]
path = "../../citation_embed/saved_models/"
encoder = HuggingFaceEncoder(model_name=path+"jinaai/jina-embeddings-v2-base-en")
rl = RouteLayer(encoder=encoder, routes=routes)


def identify_collections(query):
    results = rl.retrieve_multiple_routes(query)
    # print(f"SCORE {results} { rl( 'am I allowed a pet?', route_filter=['Tenancy_Agreement']) }")
    # exit()
    names = []
    scores = []
    
    for result in results:
        names.append(result.name)
        scores.append(result.similarity_score)
    return names, scores
    