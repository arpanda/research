from Bio import Entrez, Medline

# 🔧 Step 1: Set your email (required by NCBI)
Entrez.email = "your.email@example.com"  # Replace with your email

# 🧠 Step 2: Define your search query (change to your actual name or ORCID)
search_term = "Panda Arijit[Author] AND (Abyzov A[Author] OR Tripathy S[Author])"  # Use "Last F[Author]" or ORCID if available

# 🔍 Step 3: Search for PubMed IDs
print(f"Searching PubMed for: {search_term}")
search_handle = Entrez.esearch(db="pubmed", term=search_term, retmax=100)
search_results = Entrez.read(search_handle)
search_handle.close()

id_list = search_results["IdList"]
print(f"Found {len(id_list)} publications.")

if not id_list:
    print("No publications found.")
    exit()

# 📦 Step 2: Fetch full publication records
fetch_handle = Entrez.efetch(db="pubmed", id=id_list, rettype="medline", retmode="text")
records = Medline.parse(fetch_handle)
records = list(records)
fetch_handle.close()

# 🧾 Step 3: Process records
publications = []

for rec in records:
    title = rec.get("TI", "No title")
    
    # 🛑 Skip 'Author Correction' or similar
    if "author correction" in title.lower():
        continue

    authors = rec.get("AU", [])
    
    # 🔍 Bold 'Arijit Panda' if present (case-insensitive match)
    formatted_authors = []
    for author in authors:
        # print(author)
        if "panda a" in author.lower():
            formatted_authors.append(f"<b><i>{author}</i></b>")
        else:
            formatted_authors.append(author)
        # break

    publications.append({
        "title": title,
        "authors": ", ".join(formatted_authors),
        "journal": rec.get("JT", "Unknown Journal"),
        "year": rec.get("DP", "Unknown Year").split(" ")[0],
        "pmid": rec.get("PMID", ""),
    })

# 🌐 Step 4: Generate HTML
html_output = "<h2>My PubMed Publications</h2>\n<ul>\n"
for pub in publications:
    pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pub['pmid']}/"
    html_output += f"<li><strong>{pub['title']}</strong><br>"
    # html_output += f"{pub['authors']} — <em>{pub['journal']}, {pub['year']}</em><br>"
    html_output += f"{pub['authors']}; <em><b>{pub['journal']}, {pub['year']}</b></em><br>"
    html_output += f"<a href='{pubmed_url}' target='_blank'>PubMed Link</a></li><br>\n"
html_output += "</ul>"

# 💾 Save to file
with open("pubmed_publications.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ Publication list saved to pubmed_publications.html")
