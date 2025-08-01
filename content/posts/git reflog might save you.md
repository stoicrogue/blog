---
date: 2025-07-31
tags: 
title: git reflog might save you
author:
  - Mark Molea
---
Have you ever performed a `git rebase` and realized you made a huge mistake?  Have you even deleted a branch by mistake?  If none of your changes have been pushed to a remote repo, this could mean you've lost a tremendous amount of work.

Luckily, you can recover from those situations using the `git reflog`.  

> **git-reflog**
> 
> This command manages the information recorded in the reflogs.
> 
> Reference logs, or "reflogs", record when the tips of branches and other references were updated in the local repository. Reflogs are useful in various Git commands, to specify the old value of a reference. For example, `HEAD@{2}` means "where HEAD used to be two moves ago", `master@{one.week.ago}` means "where master used to point to one week ago in this local repository", and so on. See [gitrevisions[7]](https://git-scm.com/docs/gitrevisions) for more details.
> 
> source: https://git-scm.com/docs/git-reflog

Just like with `git log`, `reflog` has a SHA for each entry.  These SHA's can be used just like the commit SHA's in your `log`.  You can use commands like `checkout` or  `reset` with the SHA's from `reflog` to interact with your repository at essentially any point in your recent history.  So if you want to undo that `rebase` operation you just performed, you can use `reflog` to find a point in time before the `rebase` and use `reset --hard` to undo the `rebase`.  You could also create a branch based on that state of your repository.  The former would look like this:

```shell
git checkout VMP-380
Switched to branch 'VMP-380'
Your branch is up to date with 'origin/VMP-380'.

git log --oneline -n10
817adf9 (HEAD -> VMP-380, origin/VMP-380) VMP-380: Adding prod processing select privs to SA_DEV_LOADER
0b05d80 VMP-374: Exclude duplicate DC identifiers from ferring extract views (#103)
5c355de VMP-370: Add tp abbreviation to medlines mapping script (#102)
37b0f1d VMP-368: Add maintenance bin indicators to processing_867_validation_alert (#101)
a543448 VMP-367: Fix inflating line count bug in edi file summary views (#100)
1654dc1 VMP-365: Add supporting tables for ReprocessingRequests (#99)
56f439d VMP-360: Add trading_partner_file_expectations migration script (#95)
148358f VMP-362: clear maintenance bin flags from N101 SU 852 lines (#98)
dc30e73 VMP-363: 867 Forecast Example (#96)
700a7d7 VMP-364: Bulk Product Identifiers Insert (#97)

git rebase origin/main
Successfully rebased and updated refs/heads/VMP-380.

git log --oneline -n10
3f216c6 (HEAD -> VMP-380) VMP-380: Adding prod processing select privs to SA_DEV_LOADER
21bd78c (origin/main, origin/HEAD, main) VMP-382: Add Pelthos 852 ZA code mappings (part 1) (#105)
b068156 VMP-414: Add v_pelthos_launch view (#111)
15148ad VMP-406: Create WEB_DATA_CONNECTIONS table (#110)
1a186e6 VMP-394: Change LOG_ENTRIES ID from int to guid (#109)
b22965e VMP-398: Ensure blocked locations appear in consolidated sales view (#108)
ee11334 VMP-392: Add edi_997_recipient_configs table (#107)
457060c VMP-385: adjust backout_8XX_file sprocs to delete from stg_* tables (#106)
4f02b4b VMP-381: Added load time to invalid identifiers (#104)
0b05d80 VMP-374: Exclude duplicate DC identifiers from ferring extract views (#103)

git reflog -n10
3f216c6 (HEAD -> VMP-380) HEAD@{0}: rebase (finish): returning to refs/heads/VMP-380
3f216c6 (HEAD -> VMP-380) HEAD@{1}: rebase (pick): VMP-380: Adding prod processing select privs to SA_DEV_LOADER
21bd78c (origin/main, origin/HEAD, main) HEAD@{2}: rebase (start): checkout origin/main
817adf9 (origin/VMP-380) HEAD@{3}: checkout: moving from main to VMP-380
21bd78c (origin/main, origin/HEAD, main) HEAD@{4}: pull: Fast-forward
15148ad HEAD@{5}: checkout: moving from VMP-414 to main
6e2041f HEAD@{6}: commit: VMP-414: Filter on partner abbreviation instead of name
93bfb0b HEAD@{7}: checkout: moving from main to VMP-414
15148ad HEAD@{8}: checkout: moving from VMP-414 to main
93bfb0b HEAD@{9}: commit: VMP-414: Expand log_entries value columns to be max varchar

git reset --hard 817adf9
HEAD is now at 817adf9 VMP-380: Adding prod processing select privs to SA_DEV_LOADER

git log --oneline -n10
817adf9 (HEAD -> VMP-380, origin/VMP-380) VMP-380: Adding prod processing select privs to SA_DEV_LOADER
0b05d80 VMP-374: Exclude duplicate DC identifiers from ferring extract views (#103)
5c355de VMP-370: Add tp abbreviation to medline mapping script (#102)
37b0f1d VMP-368: Add maintenance bin indicators to processing_867_validation_alert (#101)
a543448 VMP-367: Fix inflating line count bug in edi file summary views (#100)
1654dc1 VMP-365: Add supporting tables for ReprocessingRequests (#99)
56f439d VMP-360: Add trading_partner_file_expectations migration script (#95)
148358f VMP-362: clear maintenance bin flags from N101 SU 852 lines (#98)
dc30e73 VMP-363: 867 Forecast Example (#96)
700a7d7 VMP-364: Bulk Product Identifiers Insert (#97)

```

In the snippet above we:

1. checked out the `VMP-380` branch
2. rebased it with `origin/main`
3. used `reflog` to identify the SHA before the rebase
4. reset our local branch to the point immediately before the `rebase`
5. observe that the history of our branch is ended an identical state to when we initially checked out `VMP-380`

Hope this saves you some grief in the future.  I know it has saved me many times.

> **Closing Thoughts...**
> Remember, creating branches in Git is effectively free.  
> 
> When in doubt, make a new branch to experiment with.  
> 
> You can always cherry-pick your changes over to your real branch if you want those exact commits or delete the experimental branch when you're done.

