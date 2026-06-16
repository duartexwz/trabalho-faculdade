def converter_cpf(cpf):  # pragma: no cover
    cpf_formatado = "".join(filter(str.isdigit, cpf))

    cpf_formatado = cpf_formatado.zfill(11)

    return f"{cpf_formatado[:3]}.{cpf_formatado[3:6]}.{cpf_formatado[6:9]}-{cpf_formatado[9:]}"
