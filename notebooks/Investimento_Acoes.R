
###############################################################################
# CASE: INVESTIMENTO EM AÇÕES

### Instalação de bibliotecas

  # Para cálculo do VIF
  install.packages("rms")
  
  # Para cálculo do KS e AUC
  install.packages("ROCR")

### Carregamento de bibliotecas
  
  library(rms)
  library(ROCR)

### Leitura da base de dados

  dados_investimento <- read.table(file = "Investimento_Acoes.txt",
                                   sep = "\t",
                                   dec = ".",
                                   header = TRUE)

### Visualização da base de dados

  View(dados_investimento)

### Análise exploratória breve

  # Medidas resumo
  
  summary(dados_investimento)

### Análise bivariada: variável resposta vs. variáveis explicativas e safra

  # Gráficos de boxplots
  
  par(mfrow = c(1,5), cex = 1)
  boxplot(Investimento_Fixa ~ Investiu_Variavel_6M,     data = dados_investimento, col = "darkturquoise", main = "Investimento em Renda Fixa")
  boxplot(Investimento_Tesouro ~ Investiu_Variavel_6M,  data = dados_investimento, col = "darkturquoise", main = "Investimento em Tesouro")
  boxplot(Investimento_Poupanca ~ Investiu_Variavel_6M, data = dados_investimento, col = "darkturquoise", main = "Investimento em Poupança")
  boxplot(Rendimento_Liq_12M ~ Investiu_Variavel_6M,    data = dados_investimento, col = "darkturquoise", main = "Rendimento Líquido em 12M")
  boxplot(Saldo_Conta ~ Investiu_Variavel_6M,           data = dados_investimento, col = "darkturquoise", main = "Saldo em Conta")
  
### Modelo de regressão logística múltipla

  # Comando auxiliar para para omitir notação científica nos p-valores
  
  options(scipen = 999)

  # Ajuste do modelo 1: inicial
  
  regressao_1 <- glm(Investiu_Variavel_6M ~
                       Investimento_Fixa +
                       Investimento_Tesouro +
                       Investimento_Poupanca +
                       Rendimento_Liq_12M +
                       Saldo_Conta,
                     family = binomial(link = 'logit'),
                     data = dados_investimento)
  
  summary(regressao_1)

  # Ajuste do modelo 2: retirando Investimento_Tesouro
  
  regressao_2 <- glm(Investiu_Variavel_6M ~
                       Investimento_Fixa +
                       Investimento_Poupanca +
                       Rendimento_Liq_12M +
                       Saldo_Conta,
                     family = binomial(link = 'logit'),
                     data = dados_investimento)
  
  summary(regressao_2)

  # Avaliação de colinearidade no modelo 2
  
  data.frame(VIF = vif(regressao_2))
  
  # Ajuste do modelo 3: retirando Rendimento_Liq_12M (colinearidade)
  
  regressao_3 <- glm(Investiu_Variavel_6M ~
                       Investimento_Fixa +
                       Investimento_Poupanca +
                       Saldo_Conta,
                     family = binomial(link = 'logit'),
                     data = dados_investimento)
  
  summary(regressao_3)
  
  # Avaliação de colinearidade no modelo 3
  
  data.frame(VIF = vif(regressao_3))

### Aplicação do modelo 2 e definição de resposta predita

  # Aplicação do modelo na base (criação de uma nova coluna chamada "probabilidade")
  
  dados_investimento$probabilidade_modelo_2 <- predict(regressao_2,
                                                       dados_investimento,
                                                       type = "response")

  # Definição de ponto de corte (padrão: % de 1's na amostra)
  
  ponto_corte <- mean(dados_investimento$Investiu_Variavel_6M)
  ponto_corte

  # Definição da resposta predita pelo modelo (criação de uma nova coluna chamada "predito")
  
  dados_investimento$predito_modelo_2 <- as.factor(ifelse(dados_investimento$probabilidade_modelo_2 > ponto_corte, 1, 0))

### Análise de desempenho: modelo 2

  # Tabela de classificação
  
  tabela <- table(dados_investimento$Investiu_Variavel_6M, dados_investimento$predito_modelo_2)
  tabela
  
  # Acurácia
  
  (tabela[1,1] + tabela[2,2]) / sum(tabela)
  
  # Especificidade
  
  tabela[1,1] / (tabela[1,1] + tabela[1,2])
  
  # Sensibilidade
  
  tabela[2,2] / (tabela[2,1] + tabela[2,2])

  # KS
  
  pred <- prediction(dados_investimento$probabilidade_modelo_2, dados_investimento$Investiu_Variavel_6M)
  perf <- performance(pred, "tpr", "fpr")
  ks <- max(attr(perf, 'y.values')[[1]] - attr(perf, 'x.values')[[1]])
  
  print(ks)

  # AUC
  
  pred <- prediction(dados_investimento$probabilidade_modelo_2, dados_investimento$Investiu_Variavel_6M)
  auc <- performance(pred, "auc")
  auc <- auc@y.values[[1]]
  
  print(auc)
  
### Aplicação do modelo 3 e definição de resposta predita
  
  # Aplicação do modelo na base (criação de uma nova coluna chamada "probabilidade")
  
  dados_investimento$probabilidade_modelo_3 <- predict(regressao_3,
                                                       dados_investimento,
                                                       type = "response")
  
  # Definição de ponto de corte (padrão: % de 1's na amostra)
  
  ponto_corte <- mean(dados_investimento$Investiu_Variavel_6M)
  ponto_corte
  
  # Definição da resposta predita pelo modelo (criação de uma nova coluna chamada "predito")
  
  dados_investimento$predito_modelo_3 <- as.factor(ifelse(dados_investimento$probabilidade_modelo_3 > ponto_corte, 1, 0))
  
### Análise de desempenho: modelo 3
  
  # Tabela de classificação
  
  tabela <- table(dados_investimento$Investiu_Variavel_6M, dados_investimento$predito_modelo_3)
  tabela
  
  # Acurácia
  
  (tabela[1,1] + tabela[2,2]) / sum(tabela)
  
  # Especificidade
  
  tabela[1,1] / (tabela[1,1] + tabela[1,2])
  
  # Sensibilidade
  
  tabela[2,2] / (tabela[2,1] + tabela[2,2])
  
  # KS
  
  pred <- prediction(dados_investimento$probabilidade_modelo_3, dados_investimento$Investiu_Variavel_6M)
  perf <- performance(pred, "tpr", "fpr")
  ks <- max(attr(perf, 'y.values')[[1]] - attr(perf, 'x.values')[[1]])
  
  print(ks)
  
  # AUC
  
  pred <- prediction(dados_investimento$probabilidade_modelo_3, dados_investimento$Investiu_Variavel_6M)
  auc <- performance(pred, "auc")
  auc <- auc@y.values[[1]]
  
  print(auc)
  
### Intervalos de confiança

  # Escolha do beta (0 para intercepto, ou 1, 2, ... para os parâmetros referentes a cada variável explicativa)
  
  beta = 0

  # Cálculo do intervalo
  
  print("Limite inferior")
  as.numeric(regressao_3$coefficients[beta + 1] - 1.96 * coef(summary(regressao_3))[beta + 1, "Std. Error"])
  print("Limite superior")
  as.numeric(regressao_3$coefficients[beta + 1] + 1.96 * coef(summary(regressao_3))[beta + 1, "Std. Error"])

### Exemplo de uso (aplicação) do modelo

  # Criação de base de dados com um novo investidor, que tem 6.000 reais investidos em renda fixa, não tem investimento em poupança, e tem 3.000 reais de saldo em conta
  # Obs.: os nomes das colunas e padrão de conteúdo devem ser idênticos aos da base utilizada para construção do modelo
  
  novos_dados <- data.frame(Investimento_Fixa     = c(6000),
                            Investimento_Poupanca = c(0),
                            Saldo_Conta           = c(3000))

  # Aplicação do modelo
  
  novos_dados$PROB_INVESTIR_VARIAVEL <- predict(regressao_3, novos_dados, type = "response")
  View(novos_dados)
