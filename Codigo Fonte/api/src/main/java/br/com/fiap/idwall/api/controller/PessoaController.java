package br.com.fiap.idwall.api.controller;

import br.com.fiap.idwall.api.domain.pessoa.DadosListagemPessoa;
import br.com.fiap.idwall.api.domain.pessoa.Pessoa;
import br.com.fiap.idwall.api.domain.pessoa.PessoaRepository;
import br.com.fiap.idwall.api.domain.pessoa.*;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.transaction.Transactional;
import org.springframework.web.util.UriComponentsBuilder;

@RestController
@RequestMapping("/pessoas")
@SecurityRequirement(name = "bearer-key")
public class PessoaController {

	@Autowired
	private PessoaRepository repository;

	@PostMapping
	@Transactional
	public ResponseEntity cadastar(@RequestBody DadosCadastroPessoa dados, UriComponentsBuilder uriBuider) {
		var pessoa = new Pessoa(dados);
		repository.save(pessoa);

		var uri = uriBuider.path("/pessoas/{id}").buildAndExpand(pessoa.getId()).toUri();

		return ResponseEntity.created(uri).body(new DadosDetalhamentoPessoa(pessoa));

	}

	@GetMapping
	public ResponseEntity<Page<DadosListagemPessoa>> listar(@PageableDefault(size = 10, sort = {"nome"}) Pageable paginacao,
															@RequestParam(required = false) String nome) {
		Page<Pessoa> page;
		if (nome != null) {
			page = repository.findByNomeContainingIgnoreCaseAndAtivoTrue(nome, paginacao);
		} else {
			page = repository.findAllByAtivoTrue(paginacao);
		}
		var result = page.map(DadosListagemPessoa::new);
		return ResponseEntity.ok(result);
	}

	@PutMapping
	@Transactional
	public ResponseEntity atualizarInformacoes(@RequestBody DadosAtualizacaoPessoa dados) {

		var pessoa = repository.getReferenceById(dados.id());
		pessoa.atualizarInformacoes(dados);

		return ResponseEntity.ok(new DadosDetalhamentoPessoa(pessoa));

	}

	@DeleteMapping("/{id}")
	@Transactional
	public ResponseEntity excluir(@PathVariable long id) {
		var pessoa = repository.getReferenceById(id);
		pessoa.excluir();

		return ResponseEntity.noContent().build();

	}

	@GetMapping("/{id}")
	public ResponseEntity detalhar(@PathVariable long id) {
		var pessoa = repository.getReferenceById(id);
		return ResponseEntity.ok(new DadosDetalhamentoPessoa(pessoa));

	}

}
