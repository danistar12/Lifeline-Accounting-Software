<template>
	<div class="page-shell">
		<header class="page-toolbar">
			<div>
				<h1 class="page-title">Chart of Accounts</h1>
				<p class="page-subtitle">The chart of accounts will appear here.</p>
			</div>
		</header>

		<UiCard title="Chart of Accounts" subtitle="List of accounts for the selected company.">
			<div class="table-empty">Not implemented yet.</div>
		</UiCard>
	</div>
</template>

<script>
import UiCard from '@/components/ui/UiCard.vue';

export default {
	name: 'ChartOfAccounts',
	components: { UiCard }
};
</script>
