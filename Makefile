install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

hf-login:
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HF) --add-to-git-credential

push-hub:
	huggingface-cli upload MrclStk/suml-projekt-koncowy ./App --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload MrclStk/suml-projekt-koncowy ./Model Model --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload MrclStk/suml-projekt-koncowy ./Results Metrics --repo-type=space --commit-message="Sync Model"

deploy: hf-login push-hub
