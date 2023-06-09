<script lang="ts">
    export let accounts: Account[];
</script>

<div class="row">
    <h1>Account Balance</h1>
    {#each accounts as account}
        <div class="mb-3 col-12">
            <div class="card">
                <div class="card-body">
                    <a class="card-link" href={account.url}
                        ><b>{account.name}</b></a
                    >
                    <div class="card-text">{account.balance}</div>
                </div>
            </div>
        </div>
    {/each}
</div>
