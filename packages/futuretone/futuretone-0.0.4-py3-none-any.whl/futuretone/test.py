from ps4debug import PS4Debug
import core
import asyncio
import typer


async def main():
    stoich_ip = '192.168.2.116'

    ps4 = PS4Debug(stoich_ip)
    ft: core.FutureTone = await core.FutureTone.bind(ps4)
    scores = await ft.get_score_definitions()
    for s, i in scores.items():
        print(s.name, i)
    return

    notes = [
        core.NoteDef(core.Note(core.NoteType.Triangle, (69, 79))),
        #core.NoteDef(core.Note(core.NoteType.Circle, (110, 100)), core.Note(core.NoteType.Square, (100, 100))),
    ]

    note_pointers = [await ft.spawn_note(n) for n in notes]

    note_data = [await ps4.read_struct(ft.pid, p, f'<5Q2I3Q2f3I4f3I') for p in note_pointers if p > 0]

    typer.echo('\t'.join([hex(p) for p in note_pointers]) + '\n')
    for row in zip(*note_data):
        row_str = '\t'.join([hex(d) if isinstance(d, int) else str(d) for d in row])
        typer.secho(f'{row_str}', fg='green' if all(d == row[0] for d in row) else 'red')


if __name__ == '__main__':
    asyncio.run(main())

# +5C -> layer [0;10]?