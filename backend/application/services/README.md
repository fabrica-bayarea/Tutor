# Tutor/backend/application/services
Os serviços são responsáveis por implementar a lógica de negócio e coordenar operações complexas envolvendo diferentes componentes do sistema, como CRUD, extração de conteúdo de arquivos, raspagem de dados, etc.

A ideia é que haja **um serviço para cada entidade do nosso banco de dados relacional (PostgreSQL)**, mas **não** precisamos nos prender a isso. Se uma determinada operação for complexa, um serviço pode ser uma ótima forma abstrai-la (como o serviço de scraping que temos).

## service_arquivo.py
Este serviço é responsável por processar todos os arquivos recebidos para upload, passando por um pipeline minucioso de validações e processamentos.

### Arquivos X Links
Apesar de terem origens diferentes, arquivos e links têm seus conteúdos extraídos e passam a ser tratados da mesma forma. Portanto, eles passam pelo mesmo pipeline de processamento, só que em ordens diferentes.

Para **arquivos**, o fluxo é:
1. Salvar metadados no PostgreSQL
    - 1.1. Salvar os metadados do **Arquivo** no PostgreSQL
    - 1.2. Salvar os vínculos **ArquivoTurmaMateria** no PostgreSQL
2. Salvar o arquivo no diretório do professor
3. Extrair o conteúdo do arquivo utilizando a biblioteca correta de acordo com a sua extensão (PDF, DOCX, MP4, etc)
4. Indexar no ChromaDB utilizando o mesmo ID do PostgreSQL

E para **links**, o fluxo é:
1. Extrair o conteúdo do link utilizando Selenium + WebDriver
2. Salvar metadados no PostgreSQL
    - 2.1. Salvar os metadados do **Arquivo** no PostgreSQL
    - 2.2. Salvar os vínculos **ArquivoTurmaMateria** no PostgreSQL
3. Salvar o conteúdo extraído num arquivo `.txt` no diretório do professor
4. Indexar no ChromaDB utilizando o mesmo ID do PostgreSQL

A grande diferença está na ordem das etapas. Para arquivos convencionais, a extração de conteúdo vem **depois** de salvar os dados necessários no PostgreSQL, enquanto para links, a extração de conteúdo vem **antes** de salvar os dados necessários no PostgreSQL, tornando-se a primeira etapa do processo.

### def `processar_arquivo`
É a função principal, responsável por orquestrar o passo-a-passo completo para processar um arquivo. Ela chama funções menores para realizar cada uma das etapas.

Ela é chamada na rota `/upload`, e espera receber:
- Um arquivo
- O ID do professor
- Os vínculos entre turmas e matérias
    ```json
    [
        {"turma_id": uuid.UUID, "materia_id": uuid.UUID},
        {"turma_id": uuid.UUID, "materia_id": uuid.UUID},
        ...
    ]
    ```
    - Cada vínculo é um dicionário que contém o ID da turma e o ID da matéria, processados na rota antes de chamar esta função
    - **Precisamos disso para evitar ambiguidade na atribuição de matérias e turmas para os arquivos**

E então, inicia-se o pipeline de processamento do arquivo.

#### 1. Salvar metadados do arquivo no PostgreSQL
Extraímos o nome do arquivo, e então chamamos a função **`salvar_metadados_arquivo`** passando como parâmetros esse **nome** e o **ID do professor**.

A função **`salvar_metadados_arquivo`** cria uma instância do modelo de `Arquivo` e preenche os campos `titulo` e `professor_id` com os valores recebidos _(os demais campos `id` e `data_upload` são gerados automaticamente)_, e então adiciona essa nova instância ao banco de dados PostgreSQL e retorna sua estrutura completa para uso posterior no pipeline de processamento.

#### 2. Salvar o arquivo no diretório do professor
Chamamos a função **`salvar_arquivo`** passando como parâmetros o **arquivo**, o **ID do documento _(gerado na etapa anterior)_** e o **ID do professor**.

A função **`salvar_arquivo`** cria um diretório para armazenar os arquivos do professor utilizando seu ID como nome (se ainda não houver um), altera o nome do arquivo a ser salvo para torná-lo único, salva o arquivo nesse diretório, e então retorna o caminho do arquivo salvo para uso posterior no pipeline de processamento.

* Ao alterar o nome de um arquivo antes de salvá-lo, apenas inserimos o ID de documento gerado pelo PostgreSQL antes do nome original. Dessa forma, se um arquivo antes se chamava `arquivo.pdf`, ele será salvo como no nosso sistema de arquivos local como **`<ID_do_documento>_arquivo.pdf`**.

#### 3. Extrair o conteúdo do arquivo utilizando a biblioteca correta de acordo com a sua extensão (PDF, DOCX, MP4, etc)
Esta etapa usa diferentes bibliotecas dependendo do tipo de arquivo a ser processado. Se for um arquivo de **documento textual**, como PDF, DOCX, PPTX, XLSX, CSV, HTML, XHTML, TXT, MD ou MARKDOWN, ele será processado com o **Docling**. Se for um arquivo de **vídeo**, como MP4, ele será processado com o **Whisper**.

Se usarmos **Docling** para processar o arquivo, chamamos a função **`extrair_texto_markdown`**. Se usarmos **Whisper**, chamamos **`processar_video`**. Para ambos os casos, passamos o **caminho do arquivo _(fornecido na etapa anterior)_** como parâmetro.

#### 4. Indexar no ChromaDB utilizando o mesmo ID do PostgreSQL
Finalmente, chamamos a função **`salvar_documento_vetor`** passando como parâmetros:
- o **ID do documento _(gerado na primeira etapa do processamento)_**
- o **nome do arquivo _(gerado também na primeira etapa do processamento)_**
- o **ID do professor _(fornecido pela rota)_**
- os **vínculos _(fornecidos pela rota e formatados numa única string)_**
    - Por exemplo, se recebermos os vínculos:
        ```json
        [
            {"turma_id": "turma1", "materia_id": "materia1"},
            {"turma_id": "turma2", "materia_id": "materia1"},
            {"turma_id": "turma3", "materia_id": "materia2"}
        ]
        ```
        O resultado será a string: **`turma1-materia1,turma2-materia1,turma3materia2`**.
- a **data de upload _(gerada na primeira etapa do processamento)_**
- o **texto extraído _(gerado na terceira etapa do processamento)_**

A função **`salvar_documento_vetor`** salva os dados do arquivo no ChromaDB, e não retorna nada.

---

Por fim, retornamos para a rota um dicionário contendo o **ID do documento** e o **nome do arquivo**.