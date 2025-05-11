unauthorized_response = {
    401: {
        "description": "Não autorizado",
        "content": {
            "application/json": {"example": {"detail": "Usuário ou senha inválidos"}}
        },
    }
}
