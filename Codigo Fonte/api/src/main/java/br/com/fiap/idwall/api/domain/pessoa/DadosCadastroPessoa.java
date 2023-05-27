package br.com.fiap.idwall.api.domain.pessoa;

import java.math.BigDecimal;
import java.time.LocalDate;

import br.com.fiap.idwall.api.domain.crime.DadosCrime;

public record DadosCadastroPessoa(
		String nome, 
		String apelido, 
		LocalDate dataNascimento,
		BigDecimal peso, 
		BigDecimal altura, 
		String sexo, 
		String paisOrigem, 
		String nacionalidade,
		String idiomas, 
		String marcasDistintivas, 
		String corOlhos, 
		String corCabelo, 
		String mandadosPrisao,
		DadosCrime crime) {

	
	

}
