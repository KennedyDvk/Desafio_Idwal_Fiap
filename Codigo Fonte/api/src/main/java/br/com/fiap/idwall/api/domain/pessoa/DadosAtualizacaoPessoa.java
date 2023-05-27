package br.com.fiap.idwall.api.domain.pessoa;

import br.com.fiap.idwall.api.domain.crime.DadosCrime;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;
import java.time.LocalDate;

public record DadosAtualizacaoPessoa(
        @NotNull
        Long id,
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
