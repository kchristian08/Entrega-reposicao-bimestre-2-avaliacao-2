## Justificativa
1. As rotas de autenticação ficaram em `auth.py` para separar login, cadastro e logout das rotas de treino.
2. A aplicação bloqueia o acesso aos treinos verificando se existe um usuário logado na `session`.
3. Cada treino é ligado ao `usuario_id` do usuário e só pode ser editado ou excluído por ele.