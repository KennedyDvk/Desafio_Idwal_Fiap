package br.com.fiap.idwall.api.domain.crime;

import java.time.LocalDate;

public record DadosCrime(

		String tipoCrime,
		String descricao,
		LocalDate dataCrime) {

	public DadosCrime(Crime crime) {
		this(crime.getTipoCrime(), crime.getDescricao(), crime.getDataCrime());

	}
}
