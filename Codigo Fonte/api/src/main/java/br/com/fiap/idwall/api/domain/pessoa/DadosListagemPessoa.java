package br.com.fiap.idwall.api.domain.pessoa;

import br.com.fiap.idwall.api.domain.crime.DadosCrime;

import java.math.BigDecimal;
import java.time.LocalDate;

public record DadosListagemPessoa(
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

    public DadosListagemPessoa (Pessoa pessoa) {
        this(pessoa.getId(), pessoa.getNome(), pessoa.getApelido(), pessoa.getDataNascimento(), pessoa.getPeso(), pessoa.getAltura(),
                pessoa.getSexo(), pessoa.getPaisOrigem(), pessoa.getNacionalidade(), pessoa.getIdiomas(), pessoa.getMarcasDistintivas(),
                pessoa.getCorOlhos(), pessoa.getCorCabelo(), pessoa.getMandadosPrisao(), new DadosCrime(pessoa.getCrime()));
    }
}
