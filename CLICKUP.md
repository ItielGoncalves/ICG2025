# Contexto operacional — ClickUp Inpasa (VP Elétrica/Automação/Manutenção/Obras)

> **Fonte de verdade** para qualquer atuação no ClickUp do Itiel. Toda sessão
> (web, desktop, rotina) deve ler este arquivo antes de mexer em cards.
> Quando uma regra nova surgir, atualizar aqui no mesmo padrão.

## Quem é o Itiel

Itiel Cerkunvis Gonçalves — VP de Elétrica, Automação, Manutenção e Obras da
INPASA. Usa o ClickUp como sistema central de gestão de demandas.

**Lista principal — Gestão de Demandas:**

| Item | ID |
|---|---|
| List ID | `901700927858` |
| Space ID | `90170454430` |
| Folder ID | `90170571180` |

## Mapeamento de campos — o que cada termo significa

### "Vencimento" / "prazo" / "data"
Atualizar **dois campos simultaneamente** — nunca um sem o outro:

1. **`due_date`** (campo nativo) — formato `YYYY-MM-DD`.
2. **Custom field "Quando?"** (ID `4991b3bc-201d-42ca-aa79-4f40820e8f72`) —
   valor em **timestamp ms UTC**.

### "Responsável" / "quem é o responsável"
Campo customizado **"Quem?"** (ID `dc766be9-8228-45dc-a3a5-c6ca78373758`),
tipo **labels**.

> **Nunca usar o campo `assignees`** — ele não é usado operacionalmente.

UUIDs das pessoas no campo "Quem?":

| Pessoa | UUID |
|---|---|
| Itiel | `fb0f5f95-259b-4d52-a4e8-f9ecff47db76` |
| William | `bcca50fe-360d-4df4-bd8e-986321cfb42e` |
| Maicon | `1bf55c74-5dc4-4324-aa5e-062e4e37b6f6` |
| Vitor | `9170aa5b-497a-4185-bc98-dcaf8d98102c` |
| Alan | `6cc6d990-d49d-4db4-851b-1ce08fa960ca` |
| Gleyson | `4d1a31e5-6cf8-44e3-b578-a32b341a7edd` |
| Saulo | `a5a3eb18-e223-49bd-a97c-059c32019eb6` |
| Yuri | `4b84b2d5-1c52-4417-8169-7b6b6feb9725` |

### "Comentário" / "observação" / "registro" / "anotação"
Campo **`markdown_description`** (descrição principal da tarefa).
Sempre inserir a **nova entrada no topo**, no formato:

```
**DD/MM/AAAA — Autor (contexto)**
```

preservando o histórico abaixo.

### "Progresso"
Campo customizado **"Progresso?"** (ID `1dc8c066-c6b5-4723-a651-e8d8a7094f7a`),
tipo **manual_progress** (0–100).
Formato do valor: `{"current": N}` (número inteiro).

### "Relevância" / "urgência"
Campo customizado **"Relevancia?"** (ID `c3be06f2-1c7b-4134-adaa-c137f63b047b`),
tipo **labels**:

| Label | UUID |
|---|---|
| Urgente e Importante | `b6d894f4-362c-47aa-83b4-0dc630449b75` |
| Não urgente e importante | `f05c0758-3cff-4d5b-82d2-df9678d98db1` |

### "Unidade"
Campo customizado **"Unidade?"** (ID `702458a3-15ba-4f5e-bd7c-34d86e605405`),
tipo **labels**:

| Código | Unidade | UUID |
|---|---|---|
| BLS | Balsas | `87555320-20a2-49d5-81f6-4812867996a0` |
| DRD | Dourados | `ff206f9e-9d15-4de9-ae5d-1b8692dc18a0` |
| LEM | Luís Eduardo Magalhães | `ee237cba-08f6-4afe-8618-56295d6850f9` |
| SNP | Sinop | `6db748ee-5f11-482d-9cdc-fcbebf087bc0` |
| RND | Rondonópolis | `7be9aff9-eab9-4275-9cb1-a27363e859e9` |
| RVD | Rio Verde | `ee4c1a2c-c47d-4ff5-a912-9c5376d024e3` |
| MTU | Nova Mutum | `d98c45bf-5bcc-4839-b154-98c421a24750` |

## Regras operacionais

1. **Nunca apresentar cards com status "feito"** — o que está concluído não é
   relevante.
2. **Sempre ler custom fields** via `get_task` com `include: ["custom_fields"]`
   **antes de editar** — para ler o campo "Quem?" e os demais campos
   customizados corretamente.
3. **Antes de qualquer alteração**, buscar o card e **mostrar o que vai mudar
   para aprovação do Itiel**, salvo instrução explícita de executar direto.
4. **Nomes corretos:** Gleyson (não Gleison), Cláudio Roberto Sampaio, Vitor
   (planejamento).
5. **Hierarquia de decisão:** Segurança > Qualidade > Governança > TCO > Prazo.

## Como buscar cards

- **Busca por texto:** `clickup_search` com `space_ids: ["90170454430"]`.
- **Busca por unidade ou campo customizado:** `clickup_filter_tasks` com
  `list_id: 901700927858` + `custom_fields`.

> O `search` por texto às vezes retorna resultados genéricos — se não achar,
> usar `filter_tasks` filtrando pela **unidade** (campo "Unidade?") ou pelo
> **responsável** (campo "Quem?").

## Referência rápida — IDs

| Campo | ID | Tipo |
|---|---|---|
| Quando? | `4991b3bc-201d-42ca-aa79-4f40820e8f72` | date (timestamp ms UTC) |
| Quem? | `dc766be9-8228-45dc-a3a5-c6ca78373758` | labels |
| Progresso? | `1dc8c066-c6b5-4723-a651-e8d8a7094f7a` | manual_progress (0–100) |
| Relevancia? | `c3be06f2-1c7b-4134-adaa-c137f63b047b` | labels |
| Unidade? | `702458a3-15ba-4f5e-bd7c-34d86e605405` | labels |
