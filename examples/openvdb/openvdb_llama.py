import pickle
import os
from llama_index import GPTSimpleVectorIndex

assert (
    os.getenv("OPENAI_API_KEY") is not None
), "Please set the OPENAI_API_KEY environment variable."

from llama_index import download_loader
download_loader("GithubRepositoryReader")

from llama_index.readers.llamahub_modules.github_repo import GithubClient, GithubRepositoryReader

docs = None

docs = None
if os.path.exists("docs.pkl"):
    with open("docs.pkl", "rb") as f:
        docs = pickle.load(f)

if docs is None:
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        github_client,
        owner =                  "apradhana",
        repo =                   "openvdb",
        filter_directories =     (["openvdb", "openvdb_cmd"], GithubRepositoryReader.FilterType.INCLUDE),
        filter_file_extensions = ([".h", ".cc", ".cu"], GithubRepositoryReader.FilterType.INCLUDE),
        verbose =                True,
        concurrent_requests =    10,
    )

    docs = loader.load_data(branch="master")

    with open("docs.pkl", "wb") as f:
        pickle.dump(docs, f)

index = GPTSimpleVectorIndex(docs)
index.save_to_disk('openvdb_index.json')
new_index = GPTSimpleVectorIndex.load_from_disk('openvdb_index.json')
response = new_index.query("How do you iterate through an openvdb grid?")
print(response)
