import click


@click.group()
def cli():
    pass


@cli.group()
def cluster():
    pass


@cluster.command("create")
def cluster_create():
    click.echo('create cluster')


@cluster.command("modify")
def cluster_modify():
    click.echo('modify cluster')


@cluster.command("list")
def cluster_list():
    click.echo('list cluster')


@cluster.command("info")
def cluster_info():
    click.echo('info cluster')


@cluster.command("delete")
def cluster_delete():
    click.echo('delete cluster')


@cli.group()
def project():
    pass


@project.command("list")
def project_list():
    click.echo('list project')


@project.command("info")
def project_info():
    click.echo('info project')


@cli.group()
def backup():
    pass


@backup.command("create")
def backup_create():
    click.echo('create backup')


@backup.command("list")
def backup_list():
    click.echo('list backup')


@backup.command("delete")
def backup_info():
    click.echo('info backup')


@backup.command("delete")
def backup_delete():
    click.echo('delete backup')


@cli.group()
def restore():
    pass


@restore.command("create")
def restore_create():
    click.echo('create restore')


@restore.command("list")
def restore_list():
    click.echo('list restore')


@restore.command("info")
def restore_info():
    click.echo('info restore')


@restore.command("delete")
def restore_delete():
    click.echo('delete restore')


@cli.command("config")
def config():
    click.echo('config')


if __name__ == "__main__":
    cli()
