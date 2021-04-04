<template>
  <div class="home">
    <v-container>

      <!-- enter code modal -->
      <v-dialog v-model="enterCodeDialog" max-width="400">
        <v-card>

          <form @submit.prevent="enterCode()" class="px-5 py-5">
            <v-text-field type="text" v-model="user2_code" label="enter user code">
            </v-text-field>
            <v-btn class="col-12" color="primary" type="submit">Submit</v-btn>
          </form>

        </v-card>
      </v-dialog>
      <!-- end enter code dialog -->

      <v-row>
        <v-col>
          <v-row>
            <!-- chatroom column -->
            <v-col class="col-lg-3 col-md-3 col-sm-1 px-0">

              <!-- chatrooms card -->
              <v-card color="light-blue lighten-5" class="px-4 py-4" max-height="800">

                <!-- new message btn -->
                <div>
                  <v-btn color="primary" class="col-12" @click="enterCodeDialog = true">
                    New Message
                  </v-btn>
                </div>
                <!-- end new message btn -->
                
                <!-- each chatroom card -->
                <v-card class="col-12" color="light-blue lighten-4 my-2 py-1" v-for="chatroom in chatrooms"
                        :key="chatroom.chatroom_id"
                        @click="changeMessageView(chatroom.chatroom_id, chatroom.chatroom_name,
                                                  chatroom.user2_username, chatroom.user2_id)">
                  <h2>{{ chatroom.user2_username }}</h2>
                  <span v-if="chatroom.last_message.length < 20">
                    {{ chatroom.last_message_sender }}:
                    {{ chatroom.last_message }}
                  </span>
                  <span v-else>
                    {{ chatroom.last_message_sender }}:
                    {{ chatroom.last_message.substring(0, 20) + ".." }}
                  </span>
                </v-card>
                <!-- end each chatroom card -->

              </v-card>
              <!-- end chatrooms card -->
            </v-col>
            <!-- end chatrooms column -->

            <!-- messages column -->
            <v-col v-if="notNewAccount" class="col-lg-9 col-md-9 col-sm-11 px-0">
              <!-- user2 name -->
              <div>
                <v-btn color="primary" text class="col-12">
                  {{ user2_username }}
                </v-btn>
              </div>
              <!-- end user2 name -->

              <!-- message card -->
              <v-card
                color="light-blue lighten-5"
                class="px-4 py-5"
                max-height="800"
                style="overflow: auto"
                id="scroll-target"
              >
                <div style="height: 600px" class="py-4" id="scroll-content">
                  <div v-for="message in messages" :key="message.id" class="my-1">

                    <!-- sender message -->
                    <div v-if="message.sender_id == $store.state.userInfo.id"
                         :id="message.id" align="right">
                      <v-tooltip left>
                        <template v-slot:activator="{ on, attrs }">
                          <v-chip color="primary" v-bind="attrs" v-on="on">
                            {{ message.message }}
                          </v-chip>
                        </template>
                        <span>{{ message.date_sent }}</span>
                      </v-tooltip>
                    </div>
                    <!-- end sender message -->

                    <!-- receiver message -->
                    <div v-else align="left">
                      <v-tooltip right>
                        <template v-slot:activator="{ on, attrs }">
                          <v-chip  v-bind="attrs" v-on="on">
                            {{ message.message }}
                          </v-chip>
                        </template>
                        <span>{{ message.date_sent }}</span>
                      </v-tooltip>
                    </div>
                    <!-- end receiver message -->

                  </div>

                </div>
              </v-card>
              <!-- end message card -->

              <!-- send message  -->
              <v-footer class="py-0 my-2">
                <form class="col-12 py-0" @submit.prevent="sendMessage()">
                  <v-container>
                    <v-row>
                      <v-col class="col-10 col-md-11 col-sm-11">
                        <v-text-field
                          type="text"
                          label="write message"
                          v-model="sendMessageContent.text"
                          autocomplete="off"
                        ></v-text-field>
                      </v-col>

                      <v-col class="col-2 col-md-1 col-sm-1">
                        <v-btn type="submit" color="primary" class="col-12 mt-4">send</v-btn>
                      </v-col>
                    </v-row>
                  </v-container>
                </form>
              </v-footer>
              <!-- end send message -->

            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "Home",
  data() {
    return {
      user2_code: null,
      user2_username: null,
      enterCodeDialog: false,
      notNewAccount: true,

      chatrooms: [],
      firstChatroomId: null,
      messages: [],

      sendMessageContent: {
        chatroom_id: null,
        user1_id: null,
        user2_id: null,
        text: null  
      },

      chatroomName: '',
      chatSockets: []
    }
  },
  created() {
    this.getChatrooms();
    this.firstChatroomMessages();

    var self = this;

    // fetch messages for first chatroom again
    setTimeout(() => {this.firstChatroomMessages();}, 300)
  
    // display the bottom messages (scroll to bottom when page loaded)
    setTimeout(() => {
      var element = document.getElementById("scroll-target")
      element.scrollTop = element.scrollHeight
    }, 600)

    // new Web Socket instance for all chatrooms
    setTimeout(() => {

      // create websocket objects for chatrooms which have id, name, and socket instances
      for (var i = 0; i < this.chatrooms.length; i++) {
        var data = {
          chatroom_id: this.chatrooms[i].chatroom_id,
          chatroom_name: this.chatrooms[i].chatroom_name,
          socket: new WebSocket(
            'ws://localhost:8000' + '/ws/chat/' + this.chatrooms[i].chatroom_name + '/'
          )
        }
        this.chatSockets.push(data);
      }

      // tell all chatroom's sockets to listen to onmessage event and onclose event
      for (var j = 0; j < this.chatSockets.length; j++) {
        this.chatSockets[j]['socket'].onmessage = function (e) {
            // when new message arrives fetch chatrooms
           self.getChatrooms();

            // push new message to messages array
           self.messages.push(JSON.parse(e.data));

            // display the bottom messages (scroll to bottom when page loaded)
            // after 0.4s
           setTimeout(() => {
             document.getElementById("scroll-target").scrollTop = document.getElementById("scroll-target").scrollHeight
           }, 400)
        }

        this.chatSockets[j]['socket'].onclose = function () {
          console.log('Chat socket closed unexpectedly')
        }
      }
    }, 1000)
  },
  methods: {
    enterCode: function () {
      axios.post("http://localhost:8000/api/enter-code/", {
          user1_code: this.$store.state.userInfo.code,
          user2_code: this.user2_code,
        })
        .then((response) => {
          var user1_id = this.$store.state.userInfo.id;
          var user2_id = response.data.user2_id;
          var chatroom_id = response.data.chatroom_id;

          // auto send 1 new message when new chatroom is created
          axios.post(`http://localhost:8000/api/send-message/${chatroom_id}/${user1_id}/${user2_id}/`,
            { text: "hello" })
            .then((response) => {
              if (response.data.success) window.location.reload();
            })
        })
    },
    getChatrooms: function () {
      axios.get(`http://localhost:8000/api/get-chatrooms/${this.$store.state.userInfo.id}/`)
      .then((response) => {
        this.chatrooms = response.data.chatrooms;

        // if user just created his/her account display nothing 
        this.checkNewAccount(this.chatrooms);

        if (this.notNewAccount) {
          this.user2_username = response.data.chatrooms[0].user2_username

          this.$store.commit("getFirstChatroomId",response.data.chatrooms[0].chatroom_id)

          this.$store.commit("getFirstChatroomUser2Id", response.data.chatrooms[0].user2_id)

          this.chatroomName = response.data.chatrooms[0].chatroom_name
        }
      });
    },

    // get messages for first chatroom when page loaded
    firstChatroomMessages: function () {
      var chatroom_id = this.$store.state.firstChatroomId;
      this.sendMessageContent.chatroom_id = this.$store.state.firstChatroomId;
      this.sendMessageContent.user2_id = this.$store.state.firstChatroomUser2Id;
      this.sendMessageContent.user1_id = this.$store.state.userInfo.id;

      axios.get(`http://localhost:8000/api/get-messages/${chatroom_id}/`)
      .then((response) => {
        this.messages = response.data.messages;

      });
    },

    checkNewAccount: function (chatrooms) {
      if (chatrooms.length == 0) this.notNewAccount = false;
    },

    // update message card when user click on chatroom 
    changeMessageView: function (chatroom_id, chatroom_name, user2_username, user2_id) {
      axios
        .get(`http://localhost:8000/api/get-messages/${chatroom_id}/`)
        .then((response) => {
          this.messages = response.data.messages;
          this.chatroomName = chatroom_name;
          this.user2_username = user2_username;
          this.sendMessageContent.chatroom_id = chatroom_id;
          this.sendMessageContent.user2_id = user2_id;
          this.sendMessageContent.user1_id = this.$store.state.userInfo.id;
          setTimeout(() => {
            document.getElementById(
              "scroll-target"
            ).scrollTop = document.getElementById("scroll-target").scrollHeight;
          }, 300);
        });
    },

    sendMessage: function () {
      axios
        .post(
          `http://localhost:8000/api/send-message/${this.sendMessageContent.chatroom_id}/${this.sendMessageContent.user1_id}/${this.sendMessageContent.user2_id}/`,
          {
            text: this.sendMessageContent.text,
          }
        )
        .then((response) => {

          setTimeout(() => {
            // web socket
            for (var i = 0; i < this.chatSockets.length; i++) {
              if (this.chatSockets[i]['chatroom_id'] == `${this.sendMessageContent.chatroom_id}`) {
                this.chatSockets[i].socket.send(JSON.stringify(response.data.message))
              }
            } 
            this.sendMessageContent.text = null;
          }, 500);
        });
    },
  },
};
</script>
