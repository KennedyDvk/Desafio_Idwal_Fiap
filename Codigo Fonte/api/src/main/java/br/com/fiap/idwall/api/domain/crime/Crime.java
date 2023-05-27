package br.com.fiap.idwall.api.domain.crime;

import java.time.LocalDate;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
@AllArgsConstructor
@Embeddable
public class Crime {


	private String tipoCrime;

	private String descricao;

	private LocalDate dataCrime;

	public Crime(DadosCrime dados) {
		this.tipoCrime = dados.tipoCrime();
		this.descricao = dados.descricao();
		this.dataCrime = dados.dataCrime();

	}


	public void atualizarInformacoes(DadosCrime dados) {
		if (dados.tipoCrime() != null) {
			this.tipoCrime = dados.tipoCrime();
		}

		if (dados.descricao() != null) {
			this.descricao = dados.descricao();
		}

		if (dados.dataCrime() != null) {
			this.dataCrime = dados.dataCrime();
		}
	}
}
