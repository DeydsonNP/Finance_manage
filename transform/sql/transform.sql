CREATE OR REPLACE TABLE financas AS

WITH 
DESPESA_ATUAL AS (
SELECT 
    "Data Lançamento" AS Data,
    'DESPESA VARIAVEIS' AS Tipo,
    "Descrição" as Descrição,
    'APP' as Categoria,
    NULL AS Valor_Real, -- Colunas não presentes em Despesas_variaveis
    CAST(REPLACE(REPLACE("Valor", '.', ''), ',', '.') AS DECIMAL) as Valor_Final,
    NULL AS Valor_a_pagar,
    'APP' AS Forma_de_Pagamento,
    'INDEFINIDO' AS Observacoes,
    TRUE AS is_pago
FROM 
    DESPESA_ATUAL
),
DESPESA_FIXA AS (
    SELECT 
        Data,
        Tipo,
        Descrição,
        Parcela,
        Categoria,
        CAST(REPLACE(REPLACE(CAST(Valor_Real AS VARCHAR), 'R$', ''), ',', '.') AS DECIMAL(10, 2)) AS Valor_Real,
        CAST(REPLACE(REPLACE(CAST(Valor_Real AS VARCHAR), 'R$', ''), ',', '.') AS DECIMAL(10, 2)) AS Valor_Final,
        CAST(REPLACE(REPLACE(CAST("Valor a Pagar" AS VARCHAR), 'R$', ''), ',', '.') AS DECIMAL(10, 2)) AS Valor_a_pagar,
        "Forma de Pagamento" AS Forma_de_Pagamento,
        UPPER(CAST(Observações AS VARCHAR)) AS Observacoes,
        CAST(is_pago AS BOOLEAN) AS is_pago
    FROM 
        DESPESA_FIXA
),
DESPESA_VARIADA AS (
    SELECT 
        Data,
        Tipo,
        Descrição,
        Categoria,
        CAST(REPLACE(REPLACE(CAST(Valor_Final AS VARCHAR), 'R$', ''), ',', '.') AS DECIMAL(10, 2)) AS Valor_Final,
        "Forma de Pagamento" AS Forma_de_Pagamento,
        UPPER(CAST(Observações AS VARCHAR)) AS Observacoes
    FROM 
        DESPESA_VARIADA
),
RECEITA_FIXA AS (
    SELECT 
        Data, 
        Tipo, 
        Descrição, 
        Categoria, 
        Valor
    FROM 
        RECEITA_FIXA
)
-- Unificando as tabelas
SELECT 
    Data,
    Tipo,
    Descrição,
    Categoria,
    Valor_Real,
    Valor_Final,
    Valor_a_pagar,
    Forma_de_Pagamento,
    Observacoes,
    is_pago
FROM 
    DESPESA_FIXA
UNION
SELECT 
    Data,
    Tipo,
    Descrição,
    Categoria,
    NULL AS Valor_Real, -- Colunas não presentes em Despesas_variaveis
    Valor_Final,
    NULL AS Valor_a_pagar,
    Forma_de_Pagamento,
    Observacoes,
    NULL AS is_pago
FROM 
    DESPESA_VARIADA
UNION
SELECT 
    Data,
    Tipo,
    Descrição,
    Categoria,
    NULL AS Valor_Real, -- Colunas não presentes em Receita_fixa
    Valor AS Valor_Final,
    NULL AS Valor_a_pagar,
    NULL AS Forma_de_Pagamento,
    NULL AS Observacoes,
    NULL AS is_pago
FROM 
    RECEITA_FIXA
UNION
SELECT 
    Data,
    Tipo,
    Descrição,
    Categoria,
    Valor_Real, -- Colunas não presentes em Receita_fixa
    ABS(Valor_Final) AS Valor_Final,
    Valor_a_pagar,
    Forma_de_Pagamento,
    Observacoes,
    is_pago
FROM 
    DESPESA_ATUAL
WHERE
    Valor_Final < 0