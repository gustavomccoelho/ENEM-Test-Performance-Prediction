## Obs.: Este é apenas um resumo do trabalho. O conteúdo completo se encontra na pasta "code".

# Previsão de Desempenho de candidatos do ENEM

## Introdução

Segundo o Ministério da Educação, o ENEM (Exame Nacional do Ensino Médio) tem o objetivo de avaliar o desempenho do estudante ao fim da escolaridade básica. Porém, o ENEM também pode atuar como uma fonte rica de informações para compreender o impacto de fatores socioeconômicos na qualidade do aprendizado de alunos do Ensino Médio. Um dos motivos para isso é a alta adesão de alunos de variados espectros sociais e econômicos. Em 2019 (sua última edição) o exame contou com a inscrição de mais de 5 milhões de candidatos, o que fornece um excelente espaço amostral da população de estudantes que desejam ingressar no ensino superior. Além disso, cada candidato é obrigado a responder uma ampla gama de perguntas em um questionário apresentado no momento da inscrição. A aplicação deste questionário resulta em 136 informações diferentes para cada um dos inscritos, incluindo informações básicas como idade, sexo e município de residência até informações detalhadas como a escolaridade dos pais, o número de banheiros na residência e o acesso à internet.

Do ponto de vista pedagógico, existem diferentes estudos que relacionam fatores socioeconômicos ao desempenho escolar. O foco deste trabalho será na utilização de métodos de Aprendizado de Máquina para prever se um dado candidato obteve um desempenho abaixo ou acima da média, com o uso das informações disponíveis resultantes do cadastro dos candidatos na edição do ENEM de 2019, além de suas respectivas notas em cada disciplina. Os dados em questão são abertos a população. 

Espera-se ao final, que o estudo resulte em um modelo eficiente (usando o menor número de variáveis possível) que permita mapear alunos com previsão de desempenho abaixo da média, podendo ser utilizados em, por exemplo, políticas públicas que visem a melhoria da qualidade do Ensino Médio e direcionadas aos alunos que precisam de apoio adicional. Os principais parâmetros utilizados para avaliar o desempenho do modelo serão a precisão e recall. Além disso, levando em consideração as variáveis sensíveis que serão usadas, é preciso certificar-se de que o modelo seja justo, ou seja, que cumpra as exigências de Data Fairness.

Após a definição do modelo, também será feita a clusterização do conjunto de dados com o objetivo de segmentar os candidatos em grupos similares de acordo com a variável alvo, e preferencialmente isolar em um segmento os candidatos com de-sempenho abaixo da média. 

## Carregamento e pré-processamento dos dados

Como já mencionado, os dados utilizados neste estudo incluem uma ampla gama de informações acerca de cada candidato, além de suas  respectivas notas. Porém, grande parte das informações são intuitivamente irrelevantes (e.g. código da prova ou solicitação de cadeira para canhoto). Há ainda variáveis com um número alto de valores ausentes, como é o caso da variável relacionada ao nome do município da escola (explicado pela grande quantidade de candidatos não matriculados em escolas no momento da inscrição). Com a eliminação destas variáveis, realiza-se a primeira grande redução, de 136 para apenas 34 variáveis. 

Para garantir a confiabilidade da análise exploratória e das etapas seguintes, é preciso tratar possíveis valores ausentes, tratar candidatos inscritos como “treineiros”, candidatos com idades incompatíveis e finalmente, discutir como agregar as notas das diferentes disciplinas para a criação da variável alvo.

### Tratamento de valores ausentes

Ao mapear os valores ausentes no conjunto de dados, nota-se que estes se encontram inteiramente concentrados nas variáveis que representam as notas dos candidatos nas diferentes disciplinas, variando em quantidade de 1,1 milhão a 1,4 milhão a depender da disciplina. Isto se deve à abstenção de candidatos em cada disciplina (de aproximadamente 27% em 2019), sendo a grande maioria destes não tendo comparecido a nenhuma das provas. A abordagem utilizada para manter a confiabilidade dos dados foi a de eliminação destes registros, o que reduziu o conjunto de dados de aproximadamente 5,1 milhões para aproximadamente 3,7 milhões de registros. 	

### Tratamento de candidatos “treineiros”

Candidatos rotulados como “treineiros” são candidatos que se inscreveram ao exame com intuito de apenas treinar seus conhecimentos. Estes candidatos, em grande maioria, representam os alunos que ainda não concluíram o Ensino Médio, e portanto não se habilitariam a ingressar ao Ensino Superior. Para manter o objetivo de analisar alunos que se habilitam a ingressar ao Ensino Superior e que passaram por todo o programa do Ensino Médio, a abordagem escolhida foi novamente de eliminação destes registros, reduzindo o conjunto de dados de 3,7 para 3,2 milhões registros. 

### Agregando notas

Existem diferenças notáveis na distribuição das notas para cada disciplina. A disciplina “Redação” possui uma densidade particular no valor zero. Estes valores são mantidos como notas válidas e não são considerados outliers ou valores ausentes. Além disso, é possível identificar uma queda de desempenho dos candidatos nas disciplinas “Matemática” e “Ciências da Natureza” (que incorpora as disciplinas Química, Biologia e Física). Como forma de simplificar a análise, propõe-se que as notas individuais sejam agregadas em médias aritméticas, calculadas para cada aluno. Esta hipótese pode apresentar limitações, principalmente em casos onde um candidato possui alta variância nos desempenhos das diferentes disciplinas. Além disso, as variáveis preditoras podem influenciar de formas desiguais as diferentes disciplinas. Por outro lado, o uso de médias contribui no tratamento de notas que se comportam como outliers. Ou seja, alunos majoritariamente acima da média podem apresentar uma nota abaixo da média sem alterar sua classificação, e vice-versa. O resultado da abordagem escolhida resulta no gráfico abaixo.

![Notas](/pictures/Notas.png)

Como visto, o formato da distribuição das médias das notas se aproxima de uma curva gaussiana.

### Tratamento de idades incompatíveis

A grande maioria da idade dos candidatos se concentra ao redor dos 20 anos, apresentando alguns outliers que devem ser tratados. Candidatos com idades superiores a 40, 60 ou até 80 anos são considerados válidos, uma vez que não existe limite superior de idade para o ingresso em universidades. Por outro lado, adota-se a hipótese de candidatos com idades inferiores a 15 anos serem muito provavelmente resultado de falhas no preenchimentos ou outliers que devem ser removidos. Portanto, o intervalo de idades considerados terá o limite inferior de 15 anos. 

### Criação da variável alvo

Para que se estabeleça a criação da variável alvo, é preciso definir um valor específico que divide os candidatos em dois grupos, i.e. candidatos com notas acima da média e candidatos com notas abaixo da média. Este valor limite é encontrado calculando a média de todas as notas após os tratamentos feitos nas etapas anteriores. Para este conjunto de dados, o valor encontrado é de 521,84. Portanto, a variável alvo é criada atribuindo valores booleanos a cada registro da seguinte forma:

  •	1 (True): Candidatos com notas abaixo de 521,84.
  •	0 (False): Candidatos com notas acima de 521,84.
  
A atribuição dos valores é feita de forma a priorizar a identificação dos candidatos abaixo da média nas métricas de desempenho do modelo, uma vez que este é o grupo de maior interesse neste trabalho.

## Feature Engineering

Após o tratamento dos dados, a etapa de feature engineering é essencial para obter informações adicionais do conjunto de dados através da criação de outras variáveis, a partir das existentes. As seguintes variáveis foram criadas:

  •	Renda per capta: Renda mensal familiar / Número de pessoas na residência.
  •	Pessoas por quarto: Número de pessoas na residência / Número de quartos.
  •	Computadores por pessoa: Número de computadores / Número de pesso-as na residência.
  •	Celulares por pessoa: Número de celulares / Número de pessoas na residência.
  
 ## Data Fairness
 
Um dos aspectos mais importantes neste contexto é a definição de Data Fairness do modelo preditivo, especialmente por considerar variáveis de alta sensibilidade, como cor, raça e sexo. Segundo O'NEIL (2016), um modelo preditivo destrutivo segue as seguintes características:

  •	Não interpretável
  •	Retroalimenta desigualdades
  •	Capacidade de crescer exponencialmente
  
Quando comparamos o modelo em questão neste trabalho com essas características, podemos chegar a alguma conclusões. Primeiramente, definimos o pré-requisito de interpretabilidade do modelo preditivo, ou seja, um candidato que tenha sido classificado com provável desempenho baixo, deve ser capaz de identificar as decisões que levaram o modelo a classifica-lo como tal. Em relação à segunda característica, fica evidente que o resultado desejado do modelo em questão é oposto ao de retroalimentar desigualdades, ou seja, se efetivamente posto em prática, o modelo ajudaria a definir os candidatos com maior probabilidade de ter um mau desempenho, norteando possíveis incentivos a estes, melhorando potencialmente seus desempenhos. Porém, é importante que este modelo não seja usado para outros fins, como identificar os alunos com maiores chances de desempenho acima da média, e premiando-os, já que isso o classificaria claramente como um modelo que retroalimenta desigualdades. Por último, a capacidade de crescer exponencialmente não parece ser aplicável neste caso, já que isso seria válido no caso da segunda característica ser verdadeira. Através destas características, define-se então que o modelo em questão cumpre os requisitos de um modelo justo, com as ressalvas feitas, e as variáveis sensíveis podem ser utilizadas.

## Tratamento das variáveis discretas

Como as variáveis do conjunto de dados são discretas e ordinais (resultado de um questionário de múltipla escolha), é necessário realizar a correta ordenação e conversão em valores numéricos. Para isso, optou-se por usar o método “Weight of Evidence”, que define o seguinte cálculo para cada categoria de uma determinada variável:
 
  𝑊𝑂𝐸=𝑙𝑛⁡(𝑃(𝑇𝑟𝑢𝑒)⁄𝑃(𝐹𝑎𝑙𝑠𝑒))
 
Ou seja, para cada categoria, seu valor será definido em uma razão entre a proporção do conjunto de dados que possuem esta categoria e resultam na variável alvo True e a proporção que resulta na variável alvo False. Dessa forma, além da ordenação das categorias, define-se também uma distância entre elas, a partir de seu comportamento em relação a variável alvo, o que será especialmente útil no momento da clusterização.

## Seleção de variáveis

Após a adição das quatro novas variáveis durante o processo de Feature Engineering, o conjunto de dados passa a contar com 38 variáveis preditoras. Espera-se que uma parte considerável destas variáveis possam ou devam ser excluídas do modelo. Para isso, utiliza-se o método de remoção recursiva.

O método de remoção recursiva se utiliza de um dado índice de importância e remove a variável do conjunto de dados recursivamente, em ordem crescente de importância. Para cada variável removida, um modelo preditivo é definido e seu desempenho é armazenado para posterior avaliação. O processo se repete até que haja apenas uma variável restante. Como método de definição das importâncias, opta-se por usar a Permutação Randômica. 

O Método da Permutação Randômica define a importância de uma variável através do uso de um modelo preditivo escolhido e em seguida permutando aleatoriamente os valores de uma determinada variável. Este método parte da suposição de que a permutação aleatória dos valores de uma variável importante deve impactar em maior magnitude o desempenho do modelo quando comparado à uma variável de menor importância. O modelo escolhido para esta etapa é o XGBoost, devido a sua alta capacidade de generalização mesmo sem alterações em seus hiperparâmetros. Com os valores de importância definidos, segue-se então com a remoção recursiva das variáveis, como visto na figura a seguir, utilizando mais uma vez o XGBoost como modelo de referência.

![Remocao_Recursiva](/pictures/Remocao_Recursiva.png)

A linha vertical do gráfico representa o corte feito entre as variáveis removidas (esquerda) e as variáveis mantidas. A figura abaixo representa a importância por permutação das 14 variáveis mantidas.

![Variaveis_Mantidas](/pictures/Variaveis_Mantidas.png)

## Análise Preditora

Na sequência, foi realisada uma análise com o objetivo de se desenvolver um modelo capaz de prever o desempenho dos candidatos com base nas variáveis socioeconômicas definidas na sessão anterior. As métricas utilizadas foram a precisão e o recall da classe 1 (Candidatos com notas abaixo da média).

Inicialmente foram testados três algoritmos de classificação diferentes, sem otimização dos hiperparâmetros: Gradient Boosting, Random Forest e Árvore de Decisão. A última apresentou o pior desempenho dos três, conforme tabela 7.1.

![Modelos](/pictures/Modelos.PNG)

No entanto, o uso de uma Árvore de Decisão para a aplicação em questão apresenta uma importante vantagem comparativa de potencializar a interpretabilidade do modelo, uma vez que essa exigência foi apontada no capítulo sobre Data Fairness. Assim, foi realizada uma análise de hiperparâmetros para melhorar o desempenho deste modelo. O parâmetro identificado como sendo mais sensível às métricas de avaliação foi o número máximo de nós da árvore. A figura 7.1 mostra como as métricas de avalição evoluem em função dele. O melhor resultado foi obtido com o número limite de 256 nós, atingindo 68,1% de precisão e 73,1% de recall. Este valor apresentou um bom trade-off entre as métricas, com 97,1% da precisão e 96,9% do recall do máximo encontrado para estas métricas com este algoritmo.

A Árvore de Decisão treinada consegue se aproximar dos outros modelos analisados e ao mesmo tempo manter algum nível de interpretabilidade, que porém, pode ser comprometido pelo elevado número de nós. Também foi realizado um ensaio utilizando-se Random Forest com árvores contendo 128 nós, mas as melhoras obtidas nas métricas foram inferiores a 1%, comparando-se com a utilização de um método ensemble com um número maior de estimadores. Este resultado corrobora a afirmação de que a Árvore de Decisão é a melhor estratégia, pois mantem certo grau de interpretabilidade, alcançando um desempenho competitivo em relação aos demais modelos.

![Numero_nos](/pictures/Numero_nos.png)

## Clusterização

Para uma melhor visualização do conjunto de dados disponível e melhor entendimento da distribuição dos dados de acordo com seus parâmetros, é preciso que haja uma redução de dimensionalidade do conjunto, reduzindo de 14 para duas variáveis, possibilitando assim a apresentação dos dados em um gráfico bidimensional. Para isso, será utilizada a técnica chamada PCA (Principal Component Analysis), que promove a redução de dimensionalidade do conjunto de dados para um número pré-definido de componentes. A implementação desta técnica no conjunto de dados em questão resulta em dois componentes com uma variância explicada de 39% em relação às variáveis originais.

Para formalizar a definição dos clusters, opta-se por usar um método de aprendizado de máquina não supervisionado conhecido por K-Means. Este método busca a segmentação dos dados de acordo com um número pré-definido de clusters, agrupando registros considerados próximos e separando registros considerados distantes (de acordo com as variáveis preditoras). Portanto, diferente de outras técnicas de clusterização, o K-Means exige que o número de segmentos seja conhecido previamente.

Para a definição inicial do número de clusters, o Método Elbow será utilizado. O método consiste na heurística da identificação do número de segmentos que promove a maior curvatura no gráfico de distorção pelo número de clusters. A intuição por trás do conceito se baseia no fato de que, apesar da distorção seguir diminuindo conforme se adicionam mais segmentos, a magnitude desta diminuição não justificaria o custo da criação de um novo segmento, após o ponto ideal dado pelo método. 

Através do Método Elbow, é possível afirmar que a maior curvatura no gráfico da distorção é encontrada na divisão do conjunto em dois segmentos. Portanto, este será o valor usado inicialmente. A figura abaixo ilustra esta representação.

![2_Clusters](/pictures/2_Clusters.png)

Apesar de haver uma clara distinção na separação dos dois clusters, ao examinar suas estatísticas percebe-se pouca representatividade em relação à variável alvo. Isso porque o cluster 1 (esquerda) inclui a grande maioria dos candidatos (75%), onde 60% possuem desempenho abaixo da média e 40% acima, enquanto o cluster 0 (direita) inclui os 25% restantes, com 80% acima da média. 

Uma maior representatividade é mais evidente ao usar-se três clusters, como visto na figura abaixo.

![3_Clusters](/pictures/3_Clusters.png)

Neste caso, temos a seguinte composição, com valores aproximados:

![Descricao_Clusters](/pictures/Descricao_Clusters.PNG)

Portanto, fica evidente que o cluster 0 contempla o segmento de candidatos com maior probabilidade de desempenho abaixo da média, o cluster 1, o segmento intermediário, e o cluster 2, os candidatos mais bem posicionados socioeconomicamente e que portanto possuem pouca probabilidade de desempenho abaixo da média.

## Conclusões e sugestões para próximos trabalhos

Como visto neste trabalho, as variáveis socioeconômicas parecem ser capazes de reconhecer no máximo 75% dos candidatos abaixo da média, com 70% de precisão, sendo possível resumir os fatores em 14 variáveis, mantendo o mesmo desempenho do modelo. A exigência de se cumprir critérios de Data Fairness leva ao requisito de interpretabilidade do modelo. Apesar do modelo usado possuir relativa alta capacidade de interpretação, é importante mencionar que o grande número de nós usado talvez prejudique este aspecto, sendo interessante analisar outras formas de prunning da árvore de decisão em futuros projetos. Uma outra abordagem interessante seria a implementação deste modelo individualmente para cada disciplina, revelando a provável variação de importância das variáveis para cada disciplina.

A clusterização dos dados através do K-Means parece resultar em segmentos mais representativos quando dividido em três clusters, diferente do número apontado pelo Método Elbow. Uma limitação nesta abordagem é a difícil interpretação desta segmentação. Isso poderia ser solucionado usando métodos de clusterização interpretáveis que também podem ser abordados em projetos futuros. 

Uma última sugestão para próximos projetos é a inclusão de variáveis não necessariamente socioeconômicas, e mais voltadas para fatores pedagógicos, como evasão escolar da região do candidato e o IDEB da escola ou município do candidato. Desta forma, talvez seja possível romper o limite de desempenho do modelo no uso exclusivo de dados socioeconômicos. 
 
