SELECT year(data_venda) AS ano,
       month(data_venda) AS mes,
       SUM(valor_total) AS vendas_totais
FROM vendas
GROUP BY year(data_venda), month(data_venda)
ORDER BY ano, mes;
