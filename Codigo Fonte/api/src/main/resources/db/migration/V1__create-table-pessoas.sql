CREATE SEQUENCE seq_pessoas START WITH 1 INCREMENT BY 1;

CREATE TABLE pessoas (
  id NUMBER DEFAULT seq_pessoas.NEXTVAL,
  nome VARCHAR2(100) NULL,
  apelido VARCHAR2(100) NULL,
  data_nascimento DATE NULL,
  peso NUMBER(10,2) NULL,
  altura NUMBER(10,2) NULL,
  sexo VARCHAR2(1) NULL,
  pais_origem VARCHAR2(100) NULL,
  nacionalidade VARCHAR2(100) NULL,
  idiomas VARCHAR2(200) NULL,
  marcas_distintivas VARCHAR2(200) NULL,
  cor_olhos VARCHAR2(50) NULL,
  cor_cabelo VARCHAR2(50) NULL,
  mandados_prisao VARCHAR2(200) NULL,
  tipo_crime VARCHAR2(255) NULL,
  descricao VARCHAR2(255) NULL,
  data_crime DATE NULL,
  CONSTRAINT pessoas_pk PRIMARY KEY (id)
);
