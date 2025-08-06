# Curriculum Translation Project

This project uses [CrewAI](https://github.com/crewAIInc/crewAI) to automate the translation of a curriculum written in [Typst](https://typst.app/), stored in a GitHub repository. The curriculum is maintained in two branches: `PT-BR` (Portuguese) and `EN` (English), each containing the respective language version. The project is available at: [https://github.com/Je-Leo-AS/Curriculo](https://github.com/Je-Leo-AS/Curriculo).

## Overview
Two GitHub Actions workflows automate the translation process:
1. **Automation Project Workflow**: A GitHub Action in the automation repository triggers on changes to the `PT-BR` branch of the curriculum repository. It sends a dispatch event to the curriculum repository.
2. **Curriculum Project Workflow**: Triggered by the dispatch event, this workflow runs the CrewAI-based translation script, which autonomously translates the curriculum from Portuguese (`PT-BR`) to English (`EN`) and updates the `EN` branch.

## Features
- Automatically translates the curriculum from Portuguese to English.
- Uses CrewAI's AI agents for collaborative translation tasks.
- Maintains separate GitHub branches: `PT-BR` for Portuguese and `EN` for English.

## How It Works
1. A change is pushed to the `PT-BR` branch of the curriculum repository.
2. The automation project's GitHub Action detects the change and sends a dispatch event to the curriculum repository.
3. The curriculum project's GitHub Action triggers, running the CrewAI script.
4. The script translates the Typst curriculum from Portuguese to English and updates the `EN` branch.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -m "Add feature"`
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.