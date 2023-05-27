CREATE SEQUENCE seq_usuarios START WITH 1 INCREMENT BY 1;

CREATE TABLE usuarios (
  id NUMBER DEFAULT seq_usuarios.NEXTVAL,
  login VARCHAR2(100) not null,
  senha VARCHAR2(255) not null,

  CONSTRAINT usuarios_pk PRIMARY KEY (id)
);
