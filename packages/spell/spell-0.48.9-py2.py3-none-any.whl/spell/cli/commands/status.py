import click

from spell.cli.exceptions import api_client_exception_handler


@click.command(name="status", short_help="Display account and billing information")
@click.option("--raw", help="Display output in raw format.", is_flag=True, default=False, hidden=True)
@click.pass_context
def status(ctx, raw):
    """
    Display account and billing information

    Display account and billing information, such as current plan, total run time,
    and free credit usage.
    """
    client = ctx.obj["client"]

    with api_client_exception_handler():
        billing_info = client.get_billing_info()

        click.echo(f"Current Plan: {billing_info.plan_name}")
        if billing_info.previous_stripe_billing_date is not None:
            click.echo(f"Previous invoice date: {billing_info.previous_stripe_billing_date}")
        if billing_info.next_stripe_billing_date is not None:
            click.echo(f"Next invoice date: {billing_info.next_stripe_billing_date}")
        if len(billing_info.period_machine_stats) > 0:
            click.echo("Upcoming charges for usage:")
            for row in billing_info.period_machine_stats:
                click.echo(f"\t- {row.machine_type_name}: {row.total.time_used} (${row.total.cost_used_usd:,.2f})")
            if billing_info.used_credits_usd > 0.0:
                click.echo(f"\t- Credits:  ($-{billing_info.used_credits_usd:,.2f})")
            click.echo(f"\t= Total:  (${billing_info.total_charge_usd:,.2f})")
        click.echo(f"Remaining free credit: ${billing_info.remaining_credits_usd:,.2f}")
        if len(billing_info.total_machine_stats) > 0:
            click.echo("Total usage:")
            for row in billing_info.total_machine_stats:
                click.echo(f"\t- {row.machine_type_name}: {row.total.time_used}")
        click.echo("Run history:")
        click.echo(f"\t- total: {billing_info.total_runs} runs")
        click.echo(f"\t- currently queued due to concurrency: {billing_info.concurrent_queued_runs} runs")
        click.echo(f"\t- plan concurrency limit: {billing_info.concurrent_run_limit} runs")
