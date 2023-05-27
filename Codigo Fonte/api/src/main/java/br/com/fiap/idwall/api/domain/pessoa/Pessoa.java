package br.com.fiap.idwall.api.domain.pessoa;

import java.math.BigDecimal;
import java.time.LocalDate;

import br.com.fiap.idwall.api.domain.crime.Crime;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Table(name = "pessoas")
@Entity(name = "Pessoa")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Pessoa {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private String nome;

	private String apelido;

	private LocalDate dataNascimento;

	private BigDecimal peso;

	private BigDecimal altura;

	private String sexo;

	private String paisOrigem;

	private String nacionalidade;

	private String idiomas;

	private String marcasDistintivas;

	private String corOlhos;

	private String corCabelo;

	private String mandadosPrisao;

	@Embedded
	private Crime crime;

	private Boolean ativo;


	public Pessoa(DadosCadastroPessoa dados) {
		this.ativo = true;
		this.nome = dados.nome();
		this.apelido = dados.apelido();
		this.dataNascimento = dados.dataNascimento();
		this.peso = dados.peso();
		this.altura = dados.altura();
		this.sexo = dados.sexo();
		this.paisOrigem = dados.paisOrigem();
		this.nacionalidade = dados.nacionalidade();
		this.idiomas = dados.idiomas();
		this.marcasDistintivas = dados.marcasDistintivas();
		this.corOlhos = dados.corOlhos();
		this.corCabelo = dados.corCabelo();
		this.mandadosPrisao = dados.mandadosPrisao();
		this.crime = new Crime(dados.crime());

	}

	public void atualizarInformacoes(DadosAtualizacaoPessoa dados) {
		if (dados.nome() != null) {
			this.nome = dados.nome();
		}

		if (dados.apelido() != null) {
			this.apelido = dados.apelido();
		}

		if (dados.dataNascimento() != null) {
			this.dataNascimento = dados.dataNascimento();
		}

		if (dados.peso() != null) {
			this.peso = dados.peso();
		}

		if (dados.altura() != null) {
			this.altura = dados.altura();
		}

		if (dados.sexo() != null) {
			this.sexo = dados.sexo();
		}

		if (dados.paisOrigem() != null) {
			this.paisOrigem = dados.paisOrigem();
		}

		if (dados.nacionalidade() != null) {
			this.nacionalidade = dados.nacionalidade();
		}

		if (dados.idiomas() != null) {
			this.idiomas = dados.idiomas();
		}

		if (dados.marcasDistintivas() != null) {
			this.marcasDistintivas = dados.marcasDistintivas();
		}

		if (dados.corOlhos() != null) {
			this.corOlhos = dados.corOlhos();
		}

		if (dados.corCabelo() != null) {
			this.corCabelo = dados.corCabelo();
		}

		if (dados.mandadosPrisao() != null) {
			this.mandadosPrisao = dados.mandadosPrisao();
		}

		if (dados.crime() != null) {
			this.crime.atualizarInformacoes(dados.crime());
		}

	}

	public void excluir() {
		this.ativo = false;
	}
}

