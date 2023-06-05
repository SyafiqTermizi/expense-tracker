<script lang="ts">
    export let accountBalance: AccountBalance;
</script>

{#each Object.keys(accountBalance) as accountName}
    <div
        class="mt-3 col-lg-{Math.ceil(
            12 / Object.keys(accountBalance).length
        )} col-md-6 col-sm-12"
    >
        <div class="card">
            <div class="card-body">
                <div class="card-title">{accountName}</div>
                <div class="card-text">{accountBalance[accountName]}</div>
            </div>
        </div>
    </div>
{/each}
