---------------------------------------------------------------------
                                USER
---------------------------------------------------------------------
user-start_info =
    Hi 👋🏻
    
    Your UID: { $telegram_id }
    Name: { $username }
    Points: { $points }
    Join date: { $join_date }
    Frens invited: { $referrals }

user-referral_link =
    Your referral link:
    { $referral_link }

user-leaderboard = 
    🏆 Top active users 🏆
    
    { $top_referrers }

user-user_rank = Your position in the ranking: { $user_rank }

user-quests-info = 
    Here you can see current subscriptions, for each of which you will receive {
        $subscription_reward -> 
        [one] { $subscription_reward } point
        *[other] { $subscription_reward } points 
    } one time 💰
    Also, each subscription to these channels will bring you {
        $checkin_reward ->
            [one] { $checkin_reward } more point
            *[other] { $checkin_reward } more points
    } for check-ins ✅

    Don't hesitate and subscribe! 😼

    { $channels }

user-quests-no_quests = There are not quests yet 😬
user-quests-already_subscribed = 
    You have already received awards for all these channels ⚠️
    Stay in touch and wait for new quests 😎

user-quests-zero_subsriptions = 
    ⚠️ You have already received rewards for your current subscriptions.
    But there are still channels to which you are not subscribed.
    Take a look closer, subscribe and get rewards! ✅💰

user-quests-subscription_reward = 
    { $points ->
        [one] Thanks for subscribing! { $points } point has been added to your account 🥳
        *[other] Thanks for subscribing! {$points } points have been credited to your account 🥳
    }

user-check_in-unsub = Tut-tut ☝🏻 You are not subscribed to any of our channels. Let's subscribe to get rewards 💰

user-check_in-reward = 
    { $points ->
        [one] You has been recieved { $points } point for check-in 🔥
        *[other] You have been recieved { $points } points for check-in 🔥 
    }
    Next check-in will be available after 24 hours ⌛️
    
user-check_in-unavailable = 
    Check-in is not available ⚠️ 
    You can check-in at { $date } UTC
---------------------------------------------------------------------
                                AUTH
---------------------------------------------------------------------
auth-start_captcha = 
    Take a simple test so that we don't consider you a robot 🤖

    Chose this collor 👉🏻 { $key_color } 👈🏻

auth-failed_captcha =
    You chose the wrong color ⚠️ Let's try again

    The new color 👉🏻 { $key_color } 👈🏻

auth-required_sub-start = 
    Great, last step left 🚀
    Subscribe to our channels to complete registration:

    { $channels }

auth-required_sub-wrong =
    You haven't subscribed to all our channels yet ⚠️
    This is a required for registration:

    { $channels }

auth-extra_messages = Please complete registration to gain access to the bot ✋🏻

auth-notify_referrer = 
    Great news! Your referral link brought in a new user 🔥
    {$points ->
        [one] You've been awarded { $points } 🥳
        *[other] You've been awarded { $points } points 🥳
    }
---------------------------------------------------------------------
                            ADMIN
---------------------------------------------------------------------
admin-wrong_link_format = Wrong link format ⚠️
admin-bot_not_admin = The bot is not the admin of this channel ⚠️
admin-channel_added = The channel successfully added ✅
admin-channel_already_added = The channel already added to the system ⚠️
admin-channel_removed = The channel successfully removed ✅
admin-channel_already_removed = The channel already removed from the system ⚠️ 
admin-newsletter_sent = The message was sent successfully ✅
admin-enter_user_points = Enter <b>telegram_id</b>=<b>points</b>:
admin-points_added = Points successfully added ✅
admin-add_points_error = An error occurred ⚠️
    Check the data is correct and try again

admin-add_channel = Enter the channel link to add ➕
admin-remove_channel = Enter the channel link to remove ➖
admin-newsletter = Enter the message for newsletter ✍🏻
admin-decide_newsletter = 
    Your newsletter message:

    "{ $newsletter }"

    Do you confirm this message?
---------------------------------------------------------------------
                            COMMON
---------------------------------------------------------------------
common-change_language = Choose language 
common-locale_changed = Language was successfully changed ✅

common-wallet_info = 
    Wallet address will be used to distribute rewards 💰

    ❗️<b>Important:</b> do not use the addresses of ByBit, Binance, etc. Otherwise, your drop will be burned 🔥

    Well suited wallets: <u>Tonkeeper, Tonhub, Ton Space</u> 👛

common-add_new_wallet = Enter your wallet address to link it to your account 👛👇🏻
common-replace_wallet = Enter a new wallet address, if you want to overwrite the current one 👛👇🏻

common-show_wallet = 
    Your wallet address:
    { $wallet }

common-show_wallet_none = 
    Your wallet address:
    None

common-wallet_added =
    The wallet is saved ✅
    You can always change your wallet address by returning here


common-info = 
    Hi 👋🏻
    Here you can earn money just by subscribing to channels and inviting friends 💰👥

    <b>How it works?</b>
    By inviting friends, subscribing to our partners and making daily check-ins, you will receive points.
    Points are the main and only indicator of your activity and contribution to the community 🫂
    The best referrers will receive rewards to the wallet (/wallet). Random active participants will also receive rewards.

    <b>About the economy:</b>
    <b>1.</b> Each subscription to channels in the "Current quests" tab will bring you {
        $subscription_reward ->
            [one] { $subscription_reward } point
            *[other] { $subscription_reward } points
        } one time.
    <b>2.</b> Each subscription to our channels or the channels of our partners will give you {
         $checkin_reward ->
            [one] { $checkin_reward } point
            *[other] { $checkin_reward } points
         } more per check-in.
    <b>3.</b> For inviting a referral you will receive {
        $invitation_reward ->
            [one] { $invitation_reward } point
            *[other] { $invitation_reward } points
         } one time.
    <b>4.</b> For each check-in and subscription of your referral, you will receive a { $referrer_part }% of his reward.

    <b>Why are there so few points for a referral?</b>
    We believe and want our community to grow with active and interested users 🔍
    Therefore, invite active users and receive part of the reward from their efforts. But also, do not forget about your own efforts to stay in the top 🏆
    We also do not want to devalue the efforts of those people who do not have the opportunity to invite many friends, but are ready to show activeness and interest in our business 🚀

    ❕You can always return to this information by entering the command /info
---------------------------------------------------------------------
                            BUTTONS
---------------------------------------------------------------------
button-admin-menu = Admin panel 🚀 
button-admin-add_channel = Add channel ➕ 
button-admin-delete_channel = Delete channel ➖
button-admin-newsletter = Newsletter ✉️ 
button-admin-confirm_newsletter = Yes 👍🏻
button-admin-cancel_newsletter = No 👎🏻
button-admin-required_channel = Required channel ✅
button-admin-optional_channel = Optional channel ✅
button-admin-dump_table = Download table 📑
button-admin-add_user_points = Add points to user 💰

button-user-ref_link = Invite frens 👥
button-user-leadearboard = Leaderboard 🏆
button-user-check_in = Check-in ✅
button-user-quests = Current quest 👾

button-common-check_subs = Check subscriptions ✅
button-common-back_to_menu = Back to menu ⬅️
button-common-start_menu = Start the main menu 💻

error-try_again = An error occurred ⚠️
    Try again please