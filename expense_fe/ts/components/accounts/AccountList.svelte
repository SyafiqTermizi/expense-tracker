<script lang="ts">
    export let accounts: Account[];
</script>

{#each accounts as account}
    <div class="mb-3 col-6">
        <div class="card">
            <div class="card-body">
                <a class="card-link" href={account.url}><b>{account.name}</b></a
                >
                <div class="card-text">RM&nbsp;{account.balance}</div>
            </div>
        </div>
    </div>
{/each}
<div class="mb-3 col-6">
    <div class="card py-2" style="background: none; border-style: dashed">
        <div class="card-body text-center">
            <a class="card-link" href="/accounts/create">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="icon icon-tabler icon-tabler-plus"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                    stroke="currentColor"
                    fill="none"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                    <path d="M12 5l0 14" />
                    <path d="M5 12l14 0" />
                </svg>
            </a>
        </div>
    </div>
</div>
