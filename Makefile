install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

hf-login:
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HF) --add-to-git-credential

push-hub:
	huggingface-cli upload MrclStk/suml-projekt-koncowy . --repo-type=space --commit-message="Full deploy" --token $(HF)

deploy: hf-login push-hub
