# KeeperRL para Windows x64

Este fork parte do repositório oficial miki151/keeperrl, commit
95d2be4e97db2243210a71918e36a533ad94dcd1 (27/10/2025).

## Baixar e executar

1. Abra Actions > Windows x64 e selecione uma execução concluída com sucesso.
2. Em Artifacts, baixe KeeperRL-Windows-x64.
3. Extraia o ZIP inteiro em uma pasta nova.
4. Execute Iniciar.bat ou keeper.exe.

Mantenha o executável, as DLLs e as pastas de dados juntos.
O pacote usa os recursos públicos do projeto e não contém o pacote comercial
de gráficos e músicas. Sem a pasta comercial data, o jogo usa o modo ASCII.
A tradução PT-BR feita anteriormente não integra este fork.

## Compilar novamente

Em Actions > Windows x64, clique Run workflow na branch master.
O workflow instala GCC e bibliotecas pelo MSYS2, compila sem Steamworks,
empacota o programa e verifica a execução de --help e o carregamento dos
dados com --gen_z_levels 1_dark_mage. O resultado da validação fica no ZIP.

A suíte interna --run_tests é desativada pelo código original em builds
RELEASE, portanto não é apresentada como validação desta compilação.
A verificação automática não substitui um teste visual e de jogabilidade
no computador do usuário.

## Alterações deste fork

- Workflow de compilação e empacotamento Windows x64.
- Adaptadores sem Steam para controles e conquistas.
- Inicialização do adaptador de entrada sem dependência da Steam.

O código e os recursos mantêm suas respectivas licenças originais.
