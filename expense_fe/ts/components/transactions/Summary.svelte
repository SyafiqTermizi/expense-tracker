<script lang="ts">
    import { summaryData } from "./store";
    import { chartColors } from "../../utils/chart";
    export let currency: string;

    const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: currency,
    });
</script>

<div class="card-body">
    <ul class="list-group list-group-flush">
        {#each Object.keys($summaryData) as category, index}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <li class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">
                        <span
                            class="badge"
                            style={`color: white; background-color: ${
                                chartColors[
                                    index >= chartColors.length
                                        ? index - chartColors.length
                                        : index
                                ]
                            }`}
                        >
                            {category}
                        </span>
                    </h6>
                    <p>
                        <b class="text-danger">
                            {formatter.format($summaryData[category].total)}
                        </b>
                        .
                        <small class="text-muted">
                            {$summaryData[category].percent} %
                        </small>
                    </p>
                </div>
            </li>
        {/each}
    </ul>
</div>
