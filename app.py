#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from crewai import Agent, Task, Crew
from crewai_tools.tools import FileReadTool 


import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# In[8]:


import os
from git import Repo

# Configurações do repositório
REPO_URL = "git@github.com:Je-Leo-AS/Curriculo.git"  # URL SSH do repositório
RESUME_DIR = os.path.join(os.getcwd(), "resume")
SSH_KEY_PATH = os.path.expanduser("~/.ssh/id_git")  # Caminho para sua chave privada SSH
BRANCH = "EN"

def setup_ssh_auth():
    """Configura autenticação SSH para Git."""
    os.environ["GIT_SSH_COMMAND"] = f"ssh -i {SSH_KEY_PATH}"

setup_ssh_auth()

# Clonar o repositório
if not os.path.exists(os.path.join(RESUME_DIR, ".git")):
    Repo.clone_from(REPO_URL, RESUME_DIR)
else:
    print(f"Repositório já existe em {RESUME_DIR}, pulando clonagem.")

# Carregar o repositório
repo = Repo(RESUME_DIR)




# In[11]:


curriculo_translated_md = 'curriculo.md'
file_typst = os.path.join(RESUME_DIR, 'main.typ')

output_md = os.path.join(os.getcwd(),curriculo_translated_md)
orig_file_tool = FileReadTool(file_typst)
typst_reader_agent = Agent(
    role="Leitor de arquivo .typ",
    goal="Ler o arquivo main.typ e identificar todo conteúdo relevante de curriulo nele como experiências etc. Escrever esse conteudo em forma de markdown ",
    backstory="Você é um especialista em análise de documentos typst, capaz de identificar e extrair texto em português de arquivos .typ com precisão.",
    tools=[orig_file_tool]
)

# Agente tradutor

translator_agent = Agent(
    role="Tradutor",
    goal="Pegar toda as partes em português do meu arquivo e traduzir para o inglês",
    backstory="Você é um tradutor experiente, capaz de traduzir de forma clara e conciza textos de portugues para ingles mantendo o tom formal.",
)

typst_reader_task = Task(
    description='ler e identificar os textos em portugues do arquivo em typst',
    expected_output='todo o conteudo texto em portugues',
    agent=typst_reader_agent,
)

translator_task = Task(
    description='tradutor de português para ingles',
    expected_output='todo o conteudo texto em portugues traduzido para inglês',
    agent=translator_agent,
    output_file=curriculo_translated_md
)

# Assemble a crew with planning enabled
crew = Crew(
    agents=[typst_reader_agent, translator_agent],
    tasks=[typst_reader_task, translator_task],
    verbose=True,
    planning=True,  # Enable planning feature
)



# In[12]:


# Executar a equipe
result = crew.kickoff()


# In[13]:


# Agente leitor de arquivos .tex e Markdown
translated_file_tool = FileReadTool(output_md)

reader_agent = Agent(
    role="Leitor de arquivos",
    goal="Ler o arquivo main.typ e curriculo.md para identificar seus conteúdos",
    backstory="Especialista em análise de documentos typst e Markdown, capaz de extrair e comparar conteúdos em idiomas diferentes com precisão." ,
    tools=[orig_file_tool, translated_file_tool], 
)

# Agente substituidor
converter_agent = Agent(
    role="Escritor documento typst",
    goal="converter o arquivo markdown typst seguindo o modelo do arquivo original substituindo o conteudo em portugues",
    backstory="Especialista em manipulação de documentos typst capaz de identificar trechos de conteudo e estrutura de um arquivo typst."
)

# Task para ler os arquivos
reader_task = Task(
    description="Ler o arquivo main.typ e curriculo.md para identificar os conteúdos",
    expected_output="Conteúdo completo do arquivo .typ e do arquivo Markdown",
    agent=reader_agent
)


# Task para substituir trechos
replacer_task = Task(
    description="Escreve um arquivo typst do meu curriculo, traduzido pro ingles, com todo conteudo do arquivo markdown em inglês porem seguindo o modelo do arquivo orginal typ",
    expected_output="Arquivo .typ com todo o conteudo do arquivo markdown seguindo o mesmo modelo do arquivo typst original,. lembre-se de escrever somente o conteudo do curriculo mais nenhuma menssagem como ```typ ... ``` e qualquer outra coisa que nao seja o conteudo do curriculo",
    agent=converter_agent,
    context=[reader_task],
    output_file='main.typ'
)

# Criar o crew
crew2 = Crew(
    agents=[reader_agent, converter_agent],
    tasks=[reader_task, replacer_task],
    verbose=True,
    planning=True
)


# In[14]:


result = crew2.kickoff()


# In[17]:


import subprocess
import shutil

# Verificar se a branch existe
remote_branch = f"origin/{BRANCH}"
if remote_branch not in [ref.name for ref in repo.references]:
    raise ValueError(f"A branch remota {remote_branch} não existe no repositório.")

repo.git.checkout(remote_branch)

shutil.move('./main.typ', file_typst)


def compile_typst(input_file):
    """Compila o arquivo Typst em PDF."""
    try:
        subprocess.run(
            ["typst", "compile", input_file],
            check=True,
            text=True,
            capture_output=True
        )
        output_file = input_file.replace('.typ', '.pdf')
        print(f"Arquivo compilado com sucesso: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao compilar: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Erro: Typst CLI não encontrado. Instale com 'typst --version'.")
        raise

compile_typst(file_typst)


# In[ ]:


if not repo.is_dirty(untracked_files=True):
    print("Nenhuma mudança para commitar.")
    
else:
    # Adicionar todas as mudanças (arquivos modificados e novos)
    repo.git.add(all=True)
    print("Arquivos adicionados ao índice do Git.")

    # Criar commit
    repo.git.commit(m="Atualiza arquivos na branch EN")
    print("Commit criado com sucesso.")


# In[20]:


# Fazer push para a branch remota
repo.git.push()
print(f"Alterações enviadas para a branch {BRANCH} no repositório remoto.")


# In[ ]:

shutil.rmtree(RESUME_DIR)

os.remove(output_md)
