from pylate import indexes, models

index = indexes.PLAID(
    index_folder="test_indexes",
    index_name="colbert",
    override=True,
)

model = models.ColBERT(
    model_name_or_path="jinaai/jina-colbert-v2",
    query_prefix="[QueryMarker]",
    document_prefix="[DocumentMarker]",
    attend_to_expansion_tokens=True,
    trust_remote_code=True,
)

documents_embeddings = model.encode(
    [
        "The nutritional profile of fruits is exceptional, containing essential vitamins, minerals, and antioxidants that support immune function. Regular consumption of diverse fruits has been linked to reduced risk of chronic diseases including heart disease, type 2 diabetes, and certain cancers. The fiber content in fruits also promotes digestive health and helps maintain healthy cholesterol levels. Nutritionists recommend consuming at least 2-3 servings of fresh fruits daily as part of a balanced diet.",
        "Recent nutritional studies have challenged traditional views on fruit consumption. While fruits contain natural sugars, their impact on blood glucose levels varies significantly based on ripeness, variety, and processing methods. The glycemic index of fruits ranges widely, with berries typically scoring lower than tropical varieties. Individuals with metabolic conditions should consider these factors when incorporating fruits into their dietary plans.",
    ],
    is_query=False,
)

index = index.add_documents(
    documents_ids=["1", "2"], documents_embeddings=documents_embeddings
)

queries_embeddings = model.encode(
    ["fruits are healthy.", "fruits are good for health and fun."],
    is_query=True,
)

matchs = index(queries_embeddings, k=10)

assert isinstance(matchs, list)
assert len(matchs) == 2
assert matchs[0][0].keys() == {"id", "score"}

queries_embeddings = model.encode(
    "fruits are healthy.",
    is_query=True,
)

matchs = index(queries_embeddings, k=10)

assert isinstance(matchs, list)
assert len(matchs) == 1
assert matchs[0][0].keys() == {"id", "score"}
