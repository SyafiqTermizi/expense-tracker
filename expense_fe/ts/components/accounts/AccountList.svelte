<script lang="ts">
    export let accounts: Account[];
</script>

{#each accounts as account}
    <div
        class="mt-3 col-lg-{Math.ceil(
            12 / Object.keys(accounts).length
        )} col-md-6 col-sm-12"
    >
        <div class="card">
            <div class="card-body">
                <a class="card-link" href={account.url}><b>{account.name}</b></a
                >
                <div class="card-text">{account.balance}</div>
            </div>
        </div>
    </div>
{/each}
