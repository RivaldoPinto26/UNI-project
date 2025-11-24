--Create DB
CREATE DATABASE TemporalDB;
GO
USE TemporalDB;
GO


-- Create Table
CREATE TABLE Funcionarios (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Nome NVARCHAR(100) NOT NULL,
    Salario DECIMAL(10,2) NOT NULL,
    SysStartTime DATETIME2 GENERATED ALWAYS AS ROW START NOT NULL,
    SysEndTime DATETIME2 GENERATED ALWAYS AS ROW END NOT NULL,
    PERIOD FOR SYSTEM_TIME (SysStartTime, SysEndTime)
)
WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.FuncionariosHistory));

GO

--Insert some Data 
INSERT INTO Funcionarios (ID, Nome, Salario) VALUES (1, 'Bruno', 1500);
UPDATE Funcionarios SET Salario = 1800 WHERE ID = 1;
UPDATE Funcionarios SET Salario = 2000 WHERE ID = 1;

-- Test in SSMS
SELECT * FROM Funcionarios;                 -- mostra os dados atuais
SELECT * FROM Funcionarios FOR SYSTEM_TIME ALL; -- mostra tudo (atuais + históricos)
