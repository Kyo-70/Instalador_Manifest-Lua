# Instalador de Arquivos .lua e .manifest

Script Python para copiar arquivos .lua e .manifest de uma pasta de origem para destinos específicos, com interface de linha de comando colorida e opção de substituição de arquivos existentes.

## 📋 Requisitos

- Python 3.6 ou superior
- Biblioteca colorama (para cores no console Windows)

## 🚀 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/Kyo-70/Instalador_Manifest-Lua.git
cd Instalador_Manifest-Lua
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

Execute o script Python:

```bash
python instalador.py
```

### Passo a Passo

1. **Pasta de Origem**: Informe o caminho da pasta onde estão os arquivos .lua e .manifest que você deseja copiar. O script irá procurar recursivamente em todas as subpastas.

2. **Contagem de Arquivos**: O script mostrará quantos arquivos .lua e .manifest foram encontrados.

3. **Destino dos Arquivos .lua**: Informe o caminho de destino para os arquivos .lua. Se o diretório não existir, o script perguntará se você deseja criá-lo.

4. **Destino dos Arquivos .manifest**: Informe o caminho de destino para os arquivos .manifest (pode ser diferente do destino dos .lua).

5. **Cópia dos Arquivos**: 
   - Se um arquivo já existir no destino, o script perguntará se você deseja substituí-lo.
   - Você pode escolher substituir (S) ou ignorar (N) cada arquivo.
   - Mensagens coloridas indicarão o sucesso ou erro de cada operação.

6. **Resumo Final**: Ao final, o script mostrará um resumo completo de quantos arquivos foram copiados, ignorados ou tiveram erros.

## 🎨 Características

- ✅ Interface colorida no terminal (funciona no Windows, Linux e Mac)
- ✅ Busca recursiva em subpastas
- ✅ Opção de criar diretórios de destino automaticamente
- ✅ Confirmação antes de substituir arquivos existentes
- ✅ Mensagens claras de sucesso e erro
- ✅ Resumo detalhado ao final da operação
- ✅ Tratamento de erros e exceções
- ✅ Cancelamento com Ctrl+C

## 📝 Exemplo de Uso

```
Pasta de origem: C:\Projetos\MeuGame\Scripts
Destino .lua: C:\Game\Scripts
Destino .manifest: C:\Game\Manifests

Resultado:
- 15 arquivos .lua copiados
- 8 arquivos .manifest copiados
- 2 arquivos ignorados (já existiam e usuário escolheu não substituir)
```

## 🛠️ Estrutura do Código

O script está organizado em funções modulares:

- `mostrar_titulo()`: Exibe o cabeçalho do programa
- `ler_diretorio_valido()`: Valida entrada de diretórios
- `contar_arquivos_por_extensao()`: Conta arquivos recursivamente
- `perguntar_sim_nao()`: Pergunta Sim/Não ao usuário
- `criar_diretorio_se_necessario()`: Cria diretórios com confirmação
- `copiar_arquivo_com_confirmacao()`: Copia arquivos com opção de substituição
- `copiar_arquivos_por_extensao()`: Processa todos os arquivos de uma extensão
- `main()`: Função principal que coordena o fluxo do programa

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente.