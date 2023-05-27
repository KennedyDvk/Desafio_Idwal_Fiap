package br.com.fiap.idwall.api.domain.pessoa;

import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Page;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PessoaRepository  extends JpaRepository<Pessoa, Long>{

    Page<Pessoa> findAllByAtivoTrue(Pageable paginacao);
    Page<Pessoa> findByNomeContainingIgnoreCaseAndAtivoTrue(String nome, Pageable pageable);
}




