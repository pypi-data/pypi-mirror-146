# Nautobot UUID Lookup Plugin

Simple to redirect existing UUIDs to the according object pages. Queries all nautobot `BaseModels`s. Fails if the models have no `get_absolute_url` method.

Usage: `https://your-nautobot-instance.com/plugins/uuid/YOUR-UUID-HERE`