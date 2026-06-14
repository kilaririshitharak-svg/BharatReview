"""
BharatReview — HuggingFace Space Deployment Script
Uploads all app code (no model weights) to the Space repo.
Run AFTER the model has been uploaded to spidy999/muril-sentiment.
"""
from huggingface_hub import HfApi
import os

TOKEN = os.environ.get("HF_TOKEN", "")   # Set HF_TOKEN env var before running
SPACE_ID = 'spidy999/BharatReview'

api = HfApi(token=TOKEN)

# Create the Space
print('Creating HuggingFace Space...')
api.create_repo(
    repo_id=SPACE_ID,
    repo_type='space',
    space_sdk='streamlit',
    private=False,
    exist_ok=True,
)
print(f'Space created: https://huggingface.co/spaces/{SPACE_ID}')

# Files to upload (code only — NO model weights)
INCLUDE_FILES = [
    'app.py',
    'inference.py',
    'analytics.py',
    'scraper.py',
    'requirements.txt',
]

# Upload the Space README card (must be named README.md in the Space repo)
SPACE_README = 'README_SPACE.md'

print('\nUploading Space README card...')
api.upload_file(
    path_or_fileobj=SPACE_README,
    path_in_repo='README.md',
    repo_id=SPACE_ID,
    repo_type='space',
    token=TOKEN,
    commit_message='Add Space README card',
)
print('  Done: README.md')

# Upload each code file
for fname in INCLUDE_FILES:
    if os.path.isfile(fname):
        size_kb = os.path.getsize(fname) / 1024
        print(f'Uploading {fname} ({size_kb:.1f} KB)...')
        api.upload_file(
            path_or_fileobj=fname,
            path_in_repo=fname,
            repo_id=SPACE_ID,
            repo_type='space',
            token=TOKEN,
            commit_message=f'Upload {fname}',
        )
        print(f'  Done: {fname}')
    else:
        print(f'  SKIPPED (not found): {fname}')

print('\n=== DEPLOYMENT COMPLETE ===')
print(f'Your app is live at: https://huggingface.co/spaces/{SPACE_ID}')
print('Note: First startup takes 2-3 minutes while HuggingFace builds the container.')
print('      Model loads on first analysis run (~40s on CPU).')
