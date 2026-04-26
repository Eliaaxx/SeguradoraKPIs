# SeguradoraKPIs - Dashboard de Performance e Perfil de Risco

Este projeto apresenta um Dashboard interativo desenvolvido em **Streamlit** para a visualização de indicadores-chave de desempenho (KPIs) de uma seguradora. O objetivo é transformar dados brutos de apólices em insights estratégicos sobre faturamento, sinistralidade e perfil demográfico dos segurados.

> **Status do Projeto:** 🚀 Versão 1.0 feita

## 🔗 Link de Acesso
(pendente)

## 🖼️ Previewb
<img width="1362" height="766" alt="image" src="https://github.com/user-attachments/assets/72df1da6-af87-41bd-b762-5d625271068d" />


## 🛠️ Tecnologias e Ferramentas
* **Linguagem:** Python
* **Manipulação de Dados:** Pandas 
* **Visualização de Dados:** Plotly Express / Graph Objects
* **Interface Web:** Streamlit
* **Deploy:** Streamlit Cloud

## 📊 O Dashboard
O painel foi desenhado com foco em UX (User Experience), utilizando um tema dark e elementos visuais modernos. As principais funcionalidades incluem:

1.  **KPI Cards:** Visualização rápida de Ticket Médio, Custo Total de Sinistros, Idade Média, Volume de Apólices e  Maior Ano de lucro
2.  **Análise de Receita:** Gráfico de barras comparando o faturamento médio (Premium) por tipo de risco.
3.  **Distribuição de Sinistros:** Gráfico circular (donut) segmentando os custos por área geográfica.
4.  **Perfil do Cliente:** Análise de tendência da idade média por segmento de risco.
5.  **Filtros Dinâmicos:** Filtros laterais que permitem segmentar toda a análise por Área e Tipo de Risco em tempo real.

## 📈 Desenvolvimento Técnico
O projeto nasceu de uma análise exploratória inicial utilizando **PySpark**, onde foram realizados tratamentos de dados, cálculos de idade e agregações complexas. Para o deploy em ambiente cloud (Streamlit Cloud), a lógica foi otimizada para **Pandas**, garantindo performance e compatibilidade.

## 📂 Estrutura do Repositório
* `app.py`: Código principal da aplicação Streamlit.
* `insurancedata.csv`: Base de dados (Dados fictícios).
* `requirements.txt`: Lista de dependências para o ambiente.
* `Analytics_Elias.ipynb`: Notebook com a análise original em PySpark.

## 🚀 Como rodar localmente
1. Clone o repositório:
   ```bash
   git clone [https://github.com/Eliaaxx/SeguradoraKPIs.git](https://github.com/Eliaaxx/SeguradoraKPIs.git)
