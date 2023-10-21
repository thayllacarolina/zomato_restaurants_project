# Projeto Zomato Restaurants

## 1. Problema de negócio:
 A empresa Zomato é uma marketplace de restaurantes, tal qual seu core business é conectar os restaurantes a seus clientes. Anunciado como um serviço de entrega de comida, jantar e descoberta de restaurantes, a marca foi fundada na Índia e está hoje presente em vários países, operando desde 2014. Os restaurantes fazem o cadastro dentro da plataforma da Zomato, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações. \
O projeto foi desenvolvido para ajudar o suposto CEO a identificar pontos chaves na empresa, fazendo uma análise dos dados e gerando um dashboard, utilizando o framework streamlit, para responder diversas perguntas.

## 2. Premissas assumidas para a análise:
Para a etapa de análise foi utilizado o dataset disponibilizado publicamente na plataforma do [Kaggle](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset/data?select=zomato.csv). Após a coleta dos dados, foram assumidas as seguintes premissas:
1.	Marketplace foi o modelo de negócio assumido.
2.	As 3 principais visões do negócio foram: visão por países, visão por cidades e visão por restaurantes/tipos de culinária.
3.	Para o caso de uma pergunta de negócio ter dois ou mais registros como resposta, foi selecionado o registro com o menor valor da coluna “Restaurant ID”, para dessa forma selecionar o restaurante que está há mais tempo cadastrado na base de dados.

## 3. Estratégia da solução
O dashboard estratégico foi desenvolvido pensando nos três principais pilares do modelo de negócio da empresa Zomato:
1.	Visão por Países;
2.	Visão por Cidades;
3.	Visão por Restaurantes/Tipos de Culinária.

Na página inicial do dashboard foram disponibilizadas as principais informações contidas na base de dados, bem como um mapa interativo com a localização dos restaurantes e informações adicionais inseridas no tooltip, podendo fazer uso dos filtros. Cada visão acima é representada pelo seguinte conjunto de métricas:
1.	Visão por Países:
    *	Quantidade de restaurantes registrados por País;
    *	Quantidade de cidades registradas por País;
    *	Estatísticas descritivas de preço para duas pessoas por País;
    *	Quantidade de restaurantes que fazem entrega por País.
2.	Visão por Cidades:
    *	Top 10 Cidades com mais restaurantes cadastrados;
    *	Top 10 Cidades com mais restaurantes com média de avaliação acima de 4;
    *	Top 10 Cidades com mais restaurantes com média de avaliação abaixo de 2,5;
    *	Top 25 Cidades com mais restaurantes 	que fazem entrega cadastrados;
    *	Top 25 Cidades com mais restaurantes que aceitam pedido online cadastrados.
3.	Visão por Restaurantes/Tipos de Culinária:
    *	Top 5 Tipos de culinária e os melhores restaurantes dessas categorias;
    *	Top 5 Tipos de culinária com mais restaurantes cadastrados;
    *	Distribuição do tipo de preço dos restaurantes;
    *	Distribuição das avaliações médias dos restaurantes;
    *	Top 15 Restaurantes com a maior avaliação média.

## 4. Top 3 Insights de dados
1.	A Zomato é de origem indiana, porém no continente americano nota-se uma grande adesão de restaurantes ao app nos EUA. Com destaque a cidade de Houston, uma das que possuem os restaurantes mais bem avaliados da plataforma.
2.	Nota-se um potencial de crescimento nos Emirados Árabes, principalmente na cidade de Abu Dhabi, que já possui uma boa quantidade de restaurantes que fazem entrega e/ou aceitam pedidos online possibilitando uma expansão e reconhecimento dos restaurantes e culinária local.
3.	Os restaurantes que aceitam pedido online são também, na média, os restaurantes que possuem mais avaliações registradas.

## 5. O produto final do projeto
Dashboard hospedado em um ambiente Cloud, disponível para acesso através de qualquer dispositivo que esteja conectado à Internet. O dashboard pode ser acessado através do seguinte link: https://zomatorestaurantsproject-thaylla.streamlit.app/

## 6. Conclusão
Esse projeto teve por objetivo criar um dashboard contendo gráficos e/ou tabelas de forma a exibir os dados e métricas da melhor forma possível para que os stakeholders pudessem analisá-los. Sendo assim, foi entregue a primeira versão como resultado do ciclo de aprendizagem de análise de dados com Python.\
Com base nas análises e no dashboard, observou-se que o app da Zomato ainda tem sua utilização muito concentrada no país de origem: Índia, porém há restaurantes de diversos países cadastrados na plataforma e há países/cidades que possuem um potencial e podem ser mais explorados através de análise de dados, possibilitando a Zomato expandir o seu negócio a nível mundial.

## 7. Próximo passos
1.	Converter os valores dos pratos para duas pessoas para uma moeda única, como por exemplo para dólar, possibilitando comparações entre diferentes países;
2.	Adicionar novos filtros para uma análise mais detalhada;
3.	Avaliar a necessidade de inserir nova visão de negócio ou alterar/atualizar alguma já existente;
4.	Identificar novos insights.
