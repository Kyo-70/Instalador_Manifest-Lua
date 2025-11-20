#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador de Arquivos .lua e .manifest
Script para copiar arquivos .lua e .manifest de uma pasta de origem para destinos específicos.
"""

import os
import shutil
from colorama import Fore, Style, init

# Inicializa colorama para funcionar no Windows
init(autoreset=True)


def mostrar_titulo():
    """Exibe o título do programa com cores"""
    print("\n" + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "  INSTALADOR DE ARQUIVOS .LUA E .MANIFEST")
    print("=" * 60)
    print(Fore.WHITE + "\nEste script copia arquivos .lua e .manifest de uma pasta")
    print("de origem para destinos específicos, com opção de substituição.")
    print("=" * 60 + "\n")


def ler_diretorio_valido(mensagem):
    """
    Solicita ao usuário um caminho de diretório e valida se existe.
    
    Args:
        mensagem (str): Mensagem a exibir ao usuário
        
    Returns:
        str: Caminho do diretório válido ou None se usuário cancelar
    """
    while True:
        print(Fore.YELLOW + mensagem)
        caminho = input(Fore.WHITE + "Caminho (ou 'sair' para encerrar): ").strip()
        
        if caminho.lower() in ['sair', 'exit', 'quit', 'q']:
            print(Fore.RED + "\nOperação cancelada pelo usuário.")
            return None
        
        if os.path.isdir(caminho):
            return os.path.abspath(caminho)
        else:
            print(Fore.RED + f"Erro: O diretório '{caminho}' não existe!")
            print(Fore.YELLOW + "Por favor, tente novamente.\n")


def contar_arquivos_por_extensao(pasta_origem, extensoes):
    """
    Conta arquivos com extensões específicas em uma pasta e subpastas.
    
    Args:
        pasta_origem (str): Caminho da pasta a percorrer
        extensoes (list): Lista de extensões a contar (ex: ['.lua', '.manifest'])
        
    Returns:
        dict: Dicionário com contagem por extensão
    """
    contagem = {ext: 0 for ext in extensoes}
    
    for raiz, dirs, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            for ext in extensoes:
                if arquivo.lower().endswith(ext.lower()):
                    contagem[ext] += 1
                    break
    
    return contagem


def perguntar_sim_nao(mensagem, cor=Fore.YELLOW):
    """
    Faz uma pergunta Sim/Não ao usuário.
    
    Args:
        mensagem (str): Mensagem da pergunta
        cor (str): Cor da mensagem (padrão: amarelo)
        
    Returns:
        bool: True para Sim, False para Não
    """
    while True:
        print(cor + mensagem + " (S/N): ", end="")
        resposta = input().strip().upper()
        
        if resposta in ['S', 'SIM', 'Y', 'YES']:
            return True
        elif resposta in ['N', 'NAO', 'NÃO', 'NO']:
            return False
        else:
            print(Fore.RED + "Resposta inválida. Digite S para Sim ou N para Não.")


def criar_diretorio_se_necessario(caminho):
    """
    Verifica se o diretório existe e, caso não exista, pergunta se deve criar.
    
    Args:
        caminho (str): Caminho do diretório
        
    Returns:
        bool: True se o diretório existe ou foi criado, False caso contrário
    """
    if os.path.isdir(caminho):
        return True
    
    print(Fore.YELLOW + f"\nO diretório '{caminho}' não existe.")
    
    if perguntar_sim_nao("Deseja criar este diretório?"):
        try:
            os.makedirs(caminho, exist_ok=True)
            print(Fore.GREEN + f"Diretório '{caminho}' criado com sucesso!")
            return True
        except Exception as e:
            print(Fore.RED + f"Erro ao criar diretório: {e}")
            return False
    else:
        return False


def copiar_arquivo_com_confirmacao(origem, destino, perguntar_substituir=True):
    """
    Copia um arquivo, com opção de confirmar substituição se já existir.
    
    Args:
        origem (str): Caminho do arquivo de origem
        destino (str): Caminho do arquivo de destino
        perguntar_substituir (bool): Se deve perguntar ao substituir arquivo existente
        
    Returns:
        str: 'copiado', 'ignorado' ou 'erro'
    """
    # Verifica se o arquivo de destino já existe
    if os.path.exists(destino) and perguntar_substituir:
        nome_arquivo = os.path.basename(destino)
        print(Fore.YELLOW + f"\n⚠ O arquivo '{nome_arquivo}' já existe no destino.")
        
        if not perguntar_sim_nao(f"Deseja SUBSTITUIR '{nome_arquivo}'?"):
            print(Fore.CYAN + f"  → Arquivo '{nome_arquivo}' ignorado.")
            return 'ignorado'
    
    # Tenta copiar o arquivo
    try:
        shutil.copy2(origem, destino)
        nome_arquivo = os.path.basename(destino)
        print(Fore.GREEN + f"  ✓ Arquivo '{nome_arquivo}' copiado com sucesso!")
        return 'copiado'
    except Exception as e:
        nome_arquivo = os.path.basename(destino)
        print(Fore.RED + f"  ✗ Erro ao copiar '{nome_arquivo}': {e}")
        return 'erro'


def copiar_arquivos_por_extensao(pasta_origem, pasta_destino, extensao):
    """
    Copia todos os arquivos de uma extensão específica para o destino.
    
    Args:
        pasta_origem (str): Pasta de origem
        pasta_destino (str): Pasta de destino
        extensao (str): Extensão dos arquivos a copiar (ex: '.lua')
        
    Returns:
        dict: Estatísticas da operação (copiados, ignorados, erros)
    """
    stats = {'copiados': 0, 'ignorados': 0, 'erros': 0}
    
    print(Fore.CYAN + Style.BRIGHT + f"\n{'=' * 60}")
    print(Fore.CYAN + Style.BRIGHT + f"  Copiando arquivos {extensao.upper()}")
    print(Fore.CYAN + Style.BRIGHT + f"{'=' * 60}\n")
    
    # Percorre a pasta de origem recursivamente
    for raiz, dirs, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            if arquivo.lower().endswith(extensao.lower()):
                origem_completa = os.path.join(raiz, arquivo)
                destino_completo = os.path.join(pasta_destino, arquivo)
                
                resultado = copiar_arquivo_com_confirmacao(origem_completa, destino_completo)
                
                if resultado == 'copiado':
                    stats['copiados'] += 1
                elif resultado == 'ignorado':
                    stats['ignorados'] += 1
                elif resultado == 'erro':
                    stats['erros'] += 1
    
    # Exibe resumo da etapa
    print(Fore.CYAN + f"\n--- Resumo da cópia de arquivos {extensao.upper()} ---")
    print(Fore.GREEN + f"  Copiados: {stats['copiados']}")
    print(Fore.YELLOW + f"  Ignorados: {stats['ignorados']}")
    print(Fore.RED + f"  Erros: {stats['erros']}")
    
    return stats


def main():
    """Função principal do programa"""
    
    # Exibe o título
    mostrar_titulo()
    
    # 1. Solicita a pasta de origem
    print(Fore.CYAN + Style.BRIGHT + "PASSO 1: Pasta de Origem")
    print("-" * 60)
    pasta_origem = ler_diretorio_valido("Informe a pasta de ORIGEM (onde estão os arquivos):")
    
    if pasta_origem is None:
        return
    
    print(Fore.GREEN + f"✓ Pasta de origem: {pasta_origem}\n")
    
    # 2. Conta os arquivos .lua e .manifest
    print(Fore.CYAN + Style.BRIGHT + "PASSO 2: Contando Arquivos")
    print("-" * 60)
    print(Fore.WHITE + "Percorrendo diretórios recursivamente...\n")
    
    contagem = contar_arquivos_por_extensao(pasta_origem, ['.lua', '.manifest'])
    
    print(Fore.MAGENTA + f"  📄 Arquivos .lua encontrados: {contagem['.lua']}")
    print(Fore.MAGENTA + f"  📄 Arquivos .manifest encontrados: {contagem['.manifest']}\n")
    
    # Verifica se há arquivos para copiar
    if contagem['.lua'] == 0 and contagem['.manifest'] == 0:
        print(Fore.RED + "⚠ Nenhum arquivo .lua ou .manifest encontrado na pasta de origem!")
        print(Fore.YELLOW + "Encerrando o programa...")
        input(Fore.WHITE + "\nPressione Enter para sair...")
        return
    
    # 3. Solicita pasta de destino para .lua (se houver arquivos .lua)
    pasta_destino_lua = None
    if contagem['.lua'] > 0:
        print(Fore.CYAN + Style.BRIGHT + "PASSO 3: Destino dos Arquivos .LUA")
        print("-" * 60)
        
        while True:
            print(Fore.YELLOW + "Informe a pasta de DESTINO para arquivos .LUA:")
            pasta_destino_lua = input(Fore.WHITE + "Caminho: ").strip()
            
            if criar_diretorio_se_necessario(pasta_destino_lua):
                pasta_destino_lua = os.path.abspath(pasta_destino_lua)
                print(Fore.GREEN + f"✓ Pasta de destino .lua: {pasta_destino_lua}\n")
                break
            else:
                print(Fore.YELLOW + "Informe outro caminho ou pressione Ctrl+C para cancelar.\n")
    
    # 4. Solicita pasta de destino para .manifest (se houver arquivos .manifest)
    pasta_destino_manifest = None
    if contagem['.manifest'] > 0:
        print(Fore.CYAN + Style.BRIGHT + "PASSO 4: Destino dos Arquivos .MANIFEST")
        print("-" * 60)
        
        while True:
            print(Fore.YELLOW + "Informe a pasta de DESTINO para arquivos .MANIFEST:")
            pasta_destino_manifest = input(Fore.WHITE + "Caminho: ").strip()
            
            if criar_diretorio_se_necessario(pasta_destino_manifest):
                pasta_destino_manifest = os.path.abspath(pasta_destino_manifest)
                print(Fore.GREEN + f"✓ Pasta de destino .manifest: {pasta_destino_manifest}\n")
                break
            else:
                print(Fore.YELLOW + "Informe outro caminho ou pressione Ctrl+C para cancelar.\n")
    
    # 5. Copia os arquivos .lua
    stats_lua = {'copiados': 0, 'ignorados': 0, 'erros': 0}
    if contagem['.lua'] > 0 and pasta_destino_lua:
        stats_lua = copiar_arquivos_por_extensao(pasta_origem, pasta_destino_lua, '.lua')
    
    # 6. Copia os arquivos .manifest
    stats_manifest = {'copiados': 0, 'ignorados': 0, 'erros': 0}
    if contagem['.manifest'] > 0 and pasta_destino_manifest:
        stats_manifest = copiar_arquivos_por_extensao(pasta_origem, pasta_destino_manifest, '.manifest')
    
    # 7. Exibe resumo final
    print(Fore.MAGENTA + Style.BRIGHT + f"\n{'=' * 60}")
    print(Fore.MAGENTA + Style.BRIGHT + "  RESUMO FINAL")
    print(Fore.MAGENTA + Style.BRIGHT + f"{'=' * 60}")
    
    print(Fore.WHITE + "\nArquivos .LUA:")
    print(Fore.GREEN + f"  ✓ Copiados: {stats_lua['copiados']}")
    print(Fore.YELLOW + f"  ⊘ Ignorados: {stats_lua['ignorados']}")
    print(Fore.RED + f"  ✗ Erros: {stats_lua['erros']}")
    
    print(Fore.WHITE + "\nArquivos .MANIFEST:")
    print(Fore.GREEN + f"  ✓ Copiados: {stats_manifest['copiados']}")
    print(Fore.YELLOW + f"  ⊘ Ignorados: {stats_manifest['ignorados']}")
    print(Fore.RED + f"  ✗ Erros: {stats_manifest['erros']}")
    
    total_copiados = stats_lua['copiados'] + stats_manifest['copiados']
    total_ignorados = stats_lua['ignorados'] + stats_manifest['ignorados']
    total_erros = stats_lua['erros'] + stats_manifest['erros']
    
    print(Fore.MAGENTA + Style.BRIGHT + f"\n{'=' * 60}")
    print(Fore.MAGENTA + Style.BRIGHT + f"  Total: {total_copiados} copiados, {total_ignorados} ignorados, {total_erros} erros")
    print(Fore.MAGENTA + Style.BRIGHT + f"{'=' * 60}")
    
    print(Fore.GREEN + Style.BRIGHT + "\n✓ Instalação concluída!")
    input(Fore.WHITE + "\nPressione Enter para sair...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n✗ Operação cancelada pelo usuário (Ctrl+C).")
        print(Fore.YELLOW + "Encerrando o programa...")
    except Exception as e:
        print(Fore.RED + f"\n\n✗ Erro inesperado: {e}")
        print(Fore.YELLOW + "Por favor, verifique e tente novamente.")
        input(Fore.WHITE + "\nPressione Enter para sair...")
